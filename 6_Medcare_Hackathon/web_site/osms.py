class OSMSService:
    def __init__(self):
        self.mock_statuses = {
            '123456789012': {'status': 'Застрахован', 'debt': '0 тг', 'last_payment': '2025.10.01'},
            '000000000000': {'status': 'Не застрахован', 'debt': '17,500 тг', 'last_payment': '2025.07.01'},
        }
        
    def check_osms_status(self, iin: str) -> dict:
        """Check OSMS status by IIN"""
        if len(iin) != 12 or not iin.isdigit():
            return {'success': False, 'message': 'Неверный формат ИИН'}
        if iin in self.mock_statuses:
            return {'success': True, 'data': self.mock_statuses[iin]}
        else:
            return {'success': True, 'data': {'status': 'Застрахован', 'debt': '0 тг', 'last_payment': '2025.11.01'}}
            
    def calculate_payment(self, income: float, employment_status: str) -> float:
        """Calculate monthly OSMS payment"""
        if employment_status == 'employed':
            return income * 0.02  # 2% for employed
        elif employment_status == 'self-employed':
            return income * 0.05  # 5% for self-employed
        else:
            return 3000  # Fixed payment for individuals

    def get_service_cost(self, service_type: str) -> int:
        """Get medical service cost"""
        costs = {
            'consultation': 15000,
            'diagnostics': 50000,
            'treatment': 100000,
            'surgery': 500000,
            'rehabilitation': 200000
        }
        return costs.get(service_type, 0)

    def get_covered_services(self, status: str) -> list:

        """Get list of covered services by status"""
        base_services = [
            'Амбулаторно-поликлиническая помощь',
            'Стационарная помощь',
            'Скорая медицинская помощь',
            'Сестринский уход'
        ]
        
        if status == 'Застрахован':
            return base_services + [
                'Высокотехнологичная диагностика',
                'Реабилитационное лечение',
                'Паллиативная помощь',
                'Профилактические осмотры'
            ]
        return base_services
