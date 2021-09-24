class ComponentManager:
    ASSIGNED_IDS = list()
    RELEASED_IDS = list()

    @classmethod
    def get_id(cls):
        if len(cls.RELEASED_IDS) == 0:
            next_id = cls.ASSIGNED_IDS[len(cls.ASSIGNED_IDS) - 1] + 1 if len(cls.ASSIGNED_IDS) > 0 else 0
            cls.ASSIGNED_IDS.append(next_id)
        else:
            next_id = cls.RELEASED_IDS.pop()
            cls.ASSIGNED_IDS = sorted(cls.ASSIGNED_IDS + [next_id])
        return next_id

    @classmethod
    def release_id(cls, component_id):
        cls.RELEASED_IDS.append(component_id)
        cls.ASSIGNED_IDS.remove(component_id)