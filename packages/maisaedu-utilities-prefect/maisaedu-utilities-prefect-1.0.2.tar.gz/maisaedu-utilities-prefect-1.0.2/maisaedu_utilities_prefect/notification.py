try:
    from prefect.engine.state import Failed

    prefect_2 = False
except Exception as e:
    prefect_2 = True

if prefect_2 is False:

    import requests
    import os

    from maisaedu_utilities_prefect.environment import get_env
    from maisaedu_utilities_prefect.constants import PRODUCTION, LOCAL, SLACK, TEAMS
    from prefect.engine.state import Failed
    from prefect.utilities.notifications import slack_notifier

    def notifier_factory(states=[Failed], type=SLACK):
        def empty_handler(obj, old_state, new_state):
            return

        def teams_handler(obj, old_state, new_state):
            if Failed in states:
                if new_state.is_failed():
                    msg = "{0} is now in a Failed state".format(obj.name)
                    url = os.environ.get("TEAMS_WEBHOOK_URL")
                    requests.post(url, json={"text": msg})

            return new_state

        if get_env() == PRODUCTION:
            if type == SLACK:
                notifier = slack_notifier(only_states=states)
            elif type == TEAMS:
                notifier = teams_handler
        elif get_env() == LOCAL:
            notifier = empty_handler

        return notifier

else:

    def notifier_factory():
        return None
