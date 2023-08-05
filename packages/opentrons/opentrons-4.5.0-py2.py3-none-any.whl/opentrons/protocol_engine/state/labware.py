"""Basic labware data state and store."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from opentrons_shared_data.deck.dev_types import DeckDefinitionV2, SlotDefV2
from opentrons_shared_data.pipette.dev_types import LabwareUri

from opentrons.types import DeckSlotName, Point
from opentrons.protocols.models import LabwareDefinition, WellDefinition
from opentrons.calibration_storage.helpers import uri_from_details

from .. import errors
from ..resources import DeckFixedLabware
from ..commands import Command, LoadLabwareResult, AddLabwareDefinitionResult
from ..types import LabwareLocation, Dimensions
from .substore import Substore, CommandReactive


@dataclass(frozen=True)
class LabwareData:
    """Labware data entry."""

    location: LabwareLocation
    uri: LabwareUri
    calibration: Tuple[float, float, float]


@dataclass(frozen=True)
class LabwareState:
    """State of all loaded labware resources."""

    labware_by_id: Dict[str, LabwareData]
    labware_definitions_by_uri: Dict[str, LabwareDefinition]
    deck_definition: DeckDefinitionV2


class LabwareStore(Substore[LabwareState], CommandReactive):
    """Labware state container."""

    _state: LabwareState

    def __init__(
        self,
        deck_definition: DeckDefinitionV2,
        deck_fixed_labware: Sequence[DeckFixedLabware],
    ) -> None:
        """Initialize a labware store and its state."""
        labware_definitions_by_uri: Dict[str, LabwareDefinition] = {
            uri_from_details(
                load_name=fixed_labware.definition.parameters.loadName,
                namespace=fixed_labware.definition.namespace,
                version=fixed_labware.definition.version,
            ): fixed_labware.definition
            for fixed_labware in deck_fixed_labware
        }
        labware_by_id = {
            fixed_labware.labware_id: LabwareData(
                location=fixed_labware.location,
                uri=uri_from_details(
                    load_name=fixed_labware.definition.parameters.loadName,
                    namespace=fixed_labware.definition.namespace,
                    version=fixed_labware.definition.version,
                ),
                calibration=(0, 0, 0),
            )
            for fixed_labware in deck_fixed_labware
        }

        self._state = LabwareState(
            labware_definitions_by_uri=labware_definitions_by_uri,
            labware_by_id=labware_by_id,
            deck_definition=deck_definition,
        )

    def handle_command(self, command: Command) -> None:
        """Modify state in reaction to a command."""
        if isinstance(command.result, LoadLabwareResult):
            uri = uri_from_details(
                namespace=command.result.definition.namespace,
                load_name=command.result.definition.parameters.loadName,
                version=command.result.definition.version,
            )
            self._state.labware_definitions_by_uri[uri] = command.result.definition
            self._state.labware_by_id[command.result.labwareId] = LabwareData(
                location=command.data.location,
                uri=uri,
                calibration=command.result.calibration,
            )
        elif isinstance(command.result, AddLabwareDefinitionResult):
            uri = uri_from_details(
                namespace=command.result.namespace,
                load_name=command.result.loadName,
                version=command.result.version,
            )
            self._state.labware_definitions_by_uri[uri] = command.data.definition


class LabwareView:
    """Read-only labware state view."""

    def __init__(self, state: LabwareState) -> None:
        """Initialize the computed view of labware state.

        Arguments:
            state: Labware state dataclass used for all calculations.
        """
        self._state = state

    def get_labware_data_by_id(self, labware_id: str) -> LabwareData:
        """Get labware data by the labware's unique identifier."""
        try:
            return self._state.labware_by_id[labware_id]
        except KeyError:
            raise errors.LabwareDoesNotExistError(f"Labware {labware_id} not found.")

    def get_labware_definition(self, labware_id: str) -> LabwareDefinition:
        """Get labware definition by the labware's unique identifier."""
        return self.get_definition_by_uri(self.get_labware_data_by_id(labware_id).uri)

    def get_deck_definition(self) -> DeckDefinitionV2:
        """Get the current deck definition."""
        return self._state.deck_definition

    def get_slot_definition(self, slot: DeckSlotName) -> SlotDefV2:
        """Get the definition of a slot in the deck."""
        deck_def = self.get_deck_definition()

        for slot_def in deck_def["locations"]["orderedSlots"]:
            if slot_def["id"] == str(slot):
                return slot_def

        raise errors.SlotDoesNotExistError(
            f"Slot ID {slot} does not exist in deck {deck_def['otId']}"
        )

    def get_slot_position(self, slot: DeckSlotName) -> Point:
        """Get the position of a deck slot."""
        slot_def = self.get_slot_definition(slot)
        position = slot_def["position"]

        return Point(x=position[0], y=position[1], z=position[2])

    def get_definition_by_uri(self, uri: LabwareUri) -> LabwareDefinition:
        """Get the labware definition matching loadName namespace and version."""
        try:
            return self._state.labware_definitions_by_uri[uri]
        except KeyError:
            raise errors.LabwareDefinitionDoesNotExistError(
                f"Labware definition for matching {uri} not found."
            )

    def get_labware_location(self, labware_id: str) -> LabwareLocation:
        """Get labware location by the labware's unique identifier."""
        return self.get_labware_data_by_id(labware_id).location

    def get_all_labware(self) -> List[Tuple[str, LabwareData]]:
        """Get a list of all labware entries in state."""
        return [entry for entry in self._state.labware_by_id.items()]

    def get_labware_has_quirk(self, labware_id: str, quirk: str) -> bool:
        """Get if a labware has a certain quirk."""
        return quirk in self.get_quirks(labware_id=labware_id)

    def get_quirks(self, labware_id: str) -> List[str]:
        """Get a labware's quirks."""
        definition = self.get_labware_definition(labware_id)
        return definition.parameters.quirks or []

    def get_well_definition(
        self,
        labware_id: str,
        well_name: str,
    ) -> WellDefinition:
        """Get a well's definition by labware and well identifier."""
        definition = self.get_labware_definition(labware_id)

        try:
            return definition.wells[well_name]
        except KeyError:
            raise errors.WellDoesNotExistError(
                f"{well_name} does not exist in {labware_id}."
            )

    def get_tip_length(self, labware_id: str) -> float:
        """Get the tip length of a tip rack."""
        definition = self.get_labware_definition(labware_id)
        if definition.parameters.tipLength is None:
            raise errors.LabwareIsNotTipRackError(
                f"Labware {labware_id} has no tip length defined."
            )
        return definition.parameters.tipLength

    def get_definition_uri(self, labware_id: str) -> str:
        """Get a labware's definition URI."""
        return self.get_labware_data_by_id(labware_id).uri

    def is_tiprack(self, labware_id: str) -> bool:
        """Get whether labware is a tiprack."""
        definition = self.get_labware_definition(labware_id)
        return definition.parameters.isTiprack

    def get_load_name(self, labware_id: str) -> str:
        """Get the labware's load name."""
        definition = self.get_labware_definition(labware_id)
        return definition.parameters.loadName

    def get_dimensions(self, labware_id: str) -> Dimensions:
        """Get the labware's dimensions."""
        definition = self.get_labware_definition(labware_id)
        dims = definition.dimensions

        return Dimensions(
            x=dims.xDimension,
            y=dims.yDimension,
            z=dims.zDimension,
        )
