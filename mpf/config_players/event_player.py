"""Event Config Player."""
from copy import deepcopy
from mpf.config_players.flat_config_player import FlatConfigPlayer
from mpf.core.delays import DelayManager
from mpf.core.utility_functions import Util


class EventPlayer(FlatConfigPlayer):

    """Posts events based on config."""

    config_file_section = 'event_player'
    show_section = 'events'

    def __init__(self, machine):
        """Initialise EventPlayer."""
        super().__init__(machine)
        self.delay = DelayManager(self.machine.delayRegistry)

    def play(self, settings, context, calling_context, priority=0, **kwargs):
        """Post (delayed) events."""
        del kwargs
        for event, s in settings.items():
            s = deepcopy(s)
            event_dict = self.machine.placeholder_manager.parse_conditional_template(event)

            if event_dict['condition'] and not event_dict['condition'].evaluate([]):
                break

            if event_dict['number']:
                delay = Util.string_to_ms(event_dict['number'])
                self.delay.add(callback=self._post_event, ms=delay,
                               event=event_dict['name'], s=s)
            else:
                self._post_event(event_dict['name'], s)

    def _post_event(self, event, s):
        self.machine.events.post(event, **s)

    def get_list_config(self, value):
        """Parse list."""
        result = {}
        for event in value:
            result[event] = {}
        return result

    def get_express_config(self, value):
        """Parse short config."""
        return self.get_list_config(Util.string_to_list(value))
