class Deputado:
    def __init__(self, id, name, salary, monthly_expenses, active_secretaries, inactive_secretaries, timestamp):
        self.id = id
        self.name = name
        self.salary = salary
        self.monthly_expenses = monthly_expenses
        self.active_secretaries = active_secretaries
        self.inactive_secretaries = inactive_secretaries
        self.timestamp = timestamp

    def to_json(self):
        return {
            'id': self.id,
            'deputado': self.name,
            'salary': self.salary if self.salary is not None else 'R$ 41.650,92',
            'montly_expenses': self.monthly_expenses,
            'active_secretaries': self.active_secretaries,
            'inactive_secretaries': self.inactive_secretaries,
            'last_update': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'built_by': 'BrasiliApp - https://brasiliapp.com.br'
        }
