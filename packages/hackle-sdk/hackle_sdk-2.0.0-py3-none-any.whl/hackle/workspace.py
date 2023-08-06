import json

from hackle.entities import *


class Workspace(object):
    def __init__(self, data):
        json_data = json.loads(data)
        bucket_id_map = self._bucket_id_map(json_data)

        self.experiment_key_map = self._experiment_key_map('AB_TEST', json_data.get('experiments', []), bucket_id_map)
        self.feature_flag_key_map = self._experiment_key_map('FEATURE_FLAG', json_data.get('featureFlags', []),
                                                             bucket_id_map)
        self.event_type_key_map = self._event_type_key_map(json_data)

    def get_experiment_or_none(self, experiment_key):
        return self.experiment_key_map.get(experiment_key)

    def get_feature_flag_or_none(self, feature_key):
        return self.feature_flag_key_map.get(feature_key)

    def get_event_type_or_none(self, event_key):
        event = self.event_type_key_map.get(event_key)

        if event:
            return event
        else:
            return EventType(0, event_key)

    @staticmethod
    def _bucket_id_map(workspace_data):
        bucket_id_map = {}
        for bucket_data in workspace_data.get('buckets', []):
            slots = []

            for slot_data in bucket_data['slots']:
                slots.append(
                    Slot(
                        start_inclusive=slot_data['startInclusive'],
                        end_exclusive=slot_data['endExclusive'],
                        variation_id=slot_data['variationId']
                    )
                )

            bucket_id_map[bucket_data['id']] = Bucket(
                seed=bucket_data['seed'],
                slot_size=bucket_data['slotSize'],
                slots=slots
            )
        return bucket_id_map

    @staticmethod
    def _experiment_key_map(experiment_type, experiments_data, bucket_id_map):
        experiment_key_map = {}
        for experiment_data in experiments_data:
            bucket = bucket_id_map[experiment_data['bucketId']]
            experiment = Workspace._experiment(experiment_type, experiment_data, bucket)
            if experiment:
                experiment_key_map[experiment_data['key']] = experiment
        return experiment_key_map

    @staticmethod
    def _experiment(type, experiment_data, bucket):
        variations = {}
        for variation_data in experiment_data['variations']:
            variations[variation_data['id']] = Variation(
                id=variation_data['id'],
                key=variation_data['key'],
                is_dropped=variation_data['status'] == 'DROPPED'
            )

        execution_data = experiment_data['execution']

        user_overrides = {}
        for override_data in execution_data['userOverrides']:
            user_overrides[override_data['userId']] = override_data['variationId']

        status = execution_data['status']
        if status == 'READY':
            return DraftExperiment(
                id=experiment_data['id'],
                key=experiment_data['key'],
                type=type,
                variations=variations,
                user_overrides=user_overrides
            )
        elif status == 'RUNNING':
            return RunningExperiment(
                id=experiment_data['id'],
                key=experiment_data['key'],
                type=type,
                variations=variations,
                user_overrides=user_overrides,
                bucket=bucket
            )
        elif status == 'PAUSED':
            return PausedExperiment(
                id=experiment_data['id'],
                key=experiment_data['key'],
                type=type,
                variations=variations,
                user_overrides=user_overrides
            )
        elif status == 'STOPPED':
            return CompletedExperiment(
                id=experiment_data['id'],
                key=experiment_data['key'],
                type=type,
                variations=variations,
                user_overrides=user_overrides,
                winner_variation_id=experiment_data['winnerVariationId']
            )

        return None

    @staticmethod
    def _event_type_key_map(json_data):
        event_type_key_map = {}
        for event_type_data in json_data.get('events', []):
            event_type_key_map[str(event_type_data['key'])] = EventType(event_type_data['id'],
                                                                        event_type_data['key'])
        return event_type_key_map
