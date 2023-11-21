from typing import List, Union
import ast


class Function:
    def __init__(self, name: str, lineNumber: int, body: list) -> None:
        self.name = name
        self.body = body
        self.lineNumber = lineNumber


class ContentExtractor(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()
        self.functions = set()

    def visit_Assign(self, node):
        # add the variable names to variables list when value assinged
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add((target.id, target.lineno))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # function body to collect lines in function
        body = []
        # go through function body and add the code to body list
        for line in node.body:
            body.append(ast.unparse(line))
        # add the function to class functions list
        self.functions.add(
            Function(name=node.name, lineNumber=node.lineno, body=body)
        )
        # add the function args to the variables name
        for target in node.args.args:
            self.variables.add((target.arg, target.lineno))
        self.generic_visit(node)


class StyleViolation:
    def __init__(
        self, message: str, line: int = None, violationType: str = None
    ) -> None:
        self.messsage = message
        self.line = line or 0
        self.violationType = violationType

    def __repr__(self) -> str:
        return (
            f"Line {self.line}: {self.messsage}"
            if self.line
            else self.messsage
        )


class Checker:
    def __init__(self, content: Union[List, None]) -> None:
        self.content = content
        self.extractor = ContentExtractor()
        if self.content:
            self.extractor.visit(ast.parse(self.content))

    @staticmethod
    def isCommentLine(line: str):
        # return true if line is comment line
        return line.strip() != "" and line.strip()[0] == "#"
    
    @staticmethod
    def isDunderMethod(name: str):
        # return True if function is dunder method
        return len(name) > 4 and name[:2] == name[-2:] == '__'

    @staticmethod
    def isEmptyLine(line: str):
        # return True when line is empty
        return line.strip() == ""

    @staticmethod
    def isCamelCased(name: str):
        # check if name is camel cased, contains only alphabetic letters
        # and doesn't include consecutive upper case letters
        if not name.isalpha():
            return False
        for i in range(len(name) - 1):
            if name[i].isupper() and name[i + 1].isupper():
                return False
        return True

    def checkAndrewId(self) -> List[StyleViolation]:
        # iterate through every comment line
        for line in self.content.splitlines():
            # check if andrew id exist in the line
            if Checker.isCommentLine(line):
                if "andrewid" in line.lower() or "andrew id" in line.lower():
                    return []
        # return Andrew ID missing violation if not found
        return [StyleViolation(message="Andrew ID is missing")]

    def checkFullName(self) -> List[StyleViolation]:
        # iterate through every comment line
        for line in self.content.splitlines():
            # check if commment contains full name info
            if Checker.isCommentLine(line):
                if "fullname" in line.lower() or "full name" in line.lower():
                    return []
        # return Full Name missing violation if not found
        return [StyleViolation(message="Full name is missing")]

    def checkVariableNames(self) -> List[StyleViolation]:
        # iterate through every variable names
        violations = []
        for variableName, lineNumber in self.extractor.variables:
            # check if variable name is not camel cased
            if not Checker.isCamelCased(name=variableName):
                violations.append(
                    StyleViolation(
                        message=f"Variable name {variableName} is not camel cased",
                        line=lineNumber,
                    )
                )
        return violations
    
    def checkLineLengths(self) -> List[StyleViolation]:
        # go through every line and check if it exceeds from 80 characters
        violations = []
        for index, line in enumerate(self.content.splitlines()):
            if len(line) > 80:
                violations.append(
                    StyleViolation(
                        message=f"Line length exceeds from 80 characters",
                        line=index + 1,
                    )
                )
        return violations
        

    def checkFunctionNames(self) -> List[StyleViolation]:
        # check every function name in the code for camel-cased
        violations = []
        for function in self.extractor.functions:
            if not (Checker.isCamelCased(name=function.name) or Checker.isDunderMethod(name=function.name)):
                violations.append(
                    StyleViolation(
                        message=f"Function name {function.name} is not camel cased",
                        line=function.lineNumber,
                    )
                )
        return violations

    def checkCommentsCount(self) -> List[StyleViolation]:
        violations = []
        numberOfComments = 0

        # count the number of total comments in the code
        for line in self.content.splitlines():
            if Checker.isCommentLine(line):
                numberOfComments += 1

        # add violation if there is no singe comment in the code
        if not numberOfComments > 0:
            violations.append(
                StyleViolation(message="Code does not contain any comments")
            )
        return violations

    def checkFunctionLengths(self) -> List[StyleViolation]:
        # check the number of code lines in every function
        violations = []
        for function in self.extractor.functions:
            # count the number of code lines un funciton
            nonEmptyLines = 0
            for line in function.body:
                if not (
                    Checker.isEmptyLine(line) or Checker.isCommentLine(line)
                ):
                    nonEmptyLines += 1
            # check if number of lines exceeds from 20
            if nonEmptyLines > 20:
                violations.append(
                    StyleViolation(
                        message=f"Function {function.name}() is more than 20 lines long",
                        line=function.lineNumber,
                    )
                )
        return violations

    def getAllViolations(self) -> List[StyleViolation]:
        if not self.content:
            return []
        # call every checker methods of parent class
        allViolations = []
        for attribute in dir(self):
            if callable(getattr(self, attribute)) and attribute.startswith(
                "check"
            ):
                # collect all the vilolations
                allViolations.extend(getattr(self, attribute)())
        # sort the style viloations by line number
        allViolations.sort(key=lambda x: x.line)
        return allViolations
