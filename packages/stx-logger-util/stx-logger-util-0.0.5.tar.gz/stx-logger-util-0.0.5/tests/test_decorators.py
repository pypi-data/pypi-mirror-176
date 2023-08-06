# Python's Libraries
import logging

# Third-party Libraries
from unittest import TestCase

# Own's Libraries
from stx_logger_util.log_admin import LogAdmin
from stx_logger_util.decorators import log
from stx_logger_util.log_admin import LogEnv


@log()
def example_Function(_parameter):
    logging.critical("Executing the example function on Production ... critical")
    logging.error("Executing the example function on Production ... error")
    logging.warning("Executing the example function on Production ... warning")
    logging.info("Executing the example function on Production ... info")
    logging.debug("Executing the example function on Production ... debug")


@log(_level=2)
def example_FunctionWithLevel(_parameter, _other_parameter=None):
    logging.critical("Executing the example function with level ... critical")
    logging.error("Executing the example function with level ... error")
    logging.warning("Executing the example function with level ... warning")
    logging.info("Executing the example function with level ... info")
    logging.debug("Executing the example function with level ... debug")


@log(_level=2.2)
def example_FunctionWithSublevel(_parameter, _other_parameter=None):
    logging.critical("Executing the example function with sublevel ... critical")
    logging.error("Executing the example function with sublevel ... error")
    logging.warning("Executing the example function with sublevel ... warning")
    logging.info("Executing the example function with sublevel ... info")
    logging.debug("Executing the example function with sublevel ... debug")


@log(_level=3)
def example_FunctionWithError(_parameter):
    raise NameError("Example Error")


class ExampleObject:

    @log()
    def get_TestData(self, _param1, _param2):
        return "ok"


class StepFunctionTest(TestCase):

    def test_Given_RequiredParams_When_EnvironmentIsProduction_Then_DontShowLogs(self):
        LogAdmin.create_Logger(LogEnv.PRODUCTION, "test1")
        example_Function("cadenita")

    def test_Given_RequiredAndTimestampParams_When_EnvironmentIsProductionAndTimestampIsFalse_Then_DontShowLogs(self):
        LogAdmin.create_Logger(LogEnv.PRODUCTION, "test2", False)
        example_Function(12)

    def test_Given_RequiredAndTimestampParams_When_EnvironmentIsProductionAndTimestampIsTrue_Then_DontShowLogs(self):
        LogAdmin.create_Logger(LogEnv.PRODUCTION, "test2", True)
        example_Function(12)

    def test_Given_RequiredParams_When_EnvironmentIsDevelopment_Then_ShowLogsWithoutTimestamp(self):
        LogAdmin.create_Logger(LogEnv.DEVELOPMENT, "test1")
        example_Function("cadenita")

    def test_Given_RequiredAndTimestapParams_When_EnvironmentIsDevelopmentAndTimestampIsFalse_Then_ShowLogsWithoutTimestamp(self):
        LogAdmin.create_Logger(LogEnv.DEVELOPMENT, "test2", False)
        example_Function(23)

    def test_Given_RequiredAndTimestapParams_When_EnvironmentIsDevelopmentAndTimestampIsTrue_Then_ShowLogsWithTimestamp(self):
        LogAdmin.create_Logger(LogEnv.DEVELOPMENT, "test2", True)
        example_Function(23)

    def test_Given_RequiredParams_When_EnvironmentIsDevelopAndFunctionHasLevel_Then_ShowLogsWithoutTimestampAndLevelDots(self):
        LogAdmin.create_Logger(LogEnv.DEVELOPMENT, "test1")
        example_FunctionWithLevel("cadenita")

    def test_Given_RequiredParams_When_EnvironmentIsDevelopAndFunctionHasSublevel_Then_ShowLogsWithoutTimestampAndSublevelDots(self):
        LogAdmin.create_Logger(LogEnv.DEVELOPMENT, "test1")
        example_FunctionWithSublevel("cadenita", "martillo")

    def test_Given_RequiredParams_When_EnvironmentIsProductionAndFunctionHasSublevelAndFail_Then_ShowLogsWithoutTimestampAndSublevelDots(self):
        LogAdmin.create_Logger(LogEnv.PRODUCTION, "test1")
        with self.assertRaises(NameError):
            example_FunctionWithError("cadenita")


class StepClassTest(TestCase):

    def test_Given_RequiredParams_When_EnvironmentIsDevelopment_Then_ShowLogs(self):
        LogAdmin.create_Logger(LogEnv.DEVELOPMENT, "test")
        example_obj = ExampleObject()
        var1 = "Parametro 1"
        var2 = "Parametro 2"
        example_obj.get_TestData(var1, var2)
