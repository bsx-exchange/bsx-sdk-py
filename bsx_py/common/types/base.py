from dataclasses import dataclass


class DataClassMeta(type):
    pass


@dataclass
class Paging:
    page: int
    per_page: int
    last_page: int
    total: int
    from_item: int
    to_item: int

    @staticmethod
    def from_dict(data: dict) -> 'Paging':
        return Paging(
            page=int(data['page']) if 'page' in data else None,
            per_page=int(data['per_page']) if 'per_page' in data else None,
            last_page=int(data['last_page']) if 'last_page' in data else None,
            total=int(data['total']) if 'total' in data else None,
            from_item=int(data['from']) if 'from' in data else None,
            to_item=int(data['to']) if 'to' in data else None,
        )
