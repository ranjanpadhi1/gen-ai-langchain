from dotenv import load_dotenv, dotenv_values
from HealthReportAnalyzer import HealthReportAnalyzer

load_dotenv()

if __name__ == '__main__':
    HealthReportAnalyzer().run()
