"""
Default implementations of AI modules
"""
from typing import Optional, List

from neighborly import World, GameObject, SimDateTime, NeighborlyEngine
from neighborly.builtin.components import LocationAliases, OpenToPublic, CurrentLocation
from neighborly.core.action import Action, AvailableActions
from neighborly.core.location import Location
from neighborly.core.routine import Routine


class DefaultMovementModule:

    def get_next_location(self, world: World, gameobject: GameObject) -> Optional[int]:
        date = world.get_resource(SimDateTime)
        routine = gameobject.try_component(Routine)
        location_aliases = gameobject.try_component(LocationAliases)

        if routine:
            routine_entry = routine.get_entry(date.weekday, date.hour)

            if (
                routine_entry
                and isinstance(routine_entry.location, str)
                and location_aliases
            ):
                return location_aliases.aliases[routine_entry.location]

            elif routine_entry:
                return int(routine_entry.location)

        potential_locations: List[int] = list(
            map(
                lambda res: res[0],
                world.get_components(Location, OpenToPublic),
            )
        )

        if potential_locations:
            return world.get_resource(NeighborlyEngine).rng.choice(potential_locations)

        return None


class DefaultSocialAIModule:

    def get_next_action(self, world: World, gameobject: GameObject) -> Optional[Action]:
        current_location_comp = gameobject.try_component(CurrentLocation)

        if current_location_comp is None:
            return None

        current_location = world.get_gameobject(current_location_comp.location)

        available_actions = current_location.try_component(AvailableActions)

        if available_actions is None:
            return None

        for action in available_actions.actions:
            ...

        return None
