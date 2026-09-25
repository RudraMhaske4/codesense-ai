class RepositoryMetrics:
    def __init__(self, scan_results):
        self.scan_results = scan_results
    def calculate(self):
        files_analyzed = 0
        total_lines = 0
        total_functions = 0
        total_classes = 0
        complexities = []
        function_lengths = []
        arguments = []
        for result in self.scan_results:
            if "error" in result:
                continue
            files_analyzed += 1
            total_lines += result.get(
                "lines_of_code", 0
            )
            total_functions += len(
                result.get("functions", [])
            )
            total_classes += len(
                result.get("classes", [])
            )
            for function in result.get(
                "functions", []
            ):
                complexities.append(
                    function.get("complexity", 1)
                )
                function_lengths.append(
                    function.get("length", 0)
                )
                arguments.append(
                    function.get("arguments", 0)
                )
        if complexities:
            average_complexity = (
                sum(complexities)
                / len(complexities)
            )
            maximum_complexity = max(
                complexities
            )
        else:
            average_complexity = 0
            maximum_complexity = 0
        if function_lengths:
            average_function_length = (
                sum(function_lengths)
                / len(function_lengths)
            )
            maximum_function_length = max(
                function_lengths
            )
        else:
            average_function_length = 0
            maximum_function_length = 0
        if arguments:
            average_arguments = (
                sum(arguments)
                / len(arguments)
            )
            maximum_arguments = max(arguments)
        else:
            average_arguments = 0
            maximum_arguments = 0
        return {
            "files_analyzed": files_analyzed,
            "total_lines_of_code": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_complexity": round(
                average_complexity, 2
            ),
            "maximum_complexity":
                maximum_complexity,
            "average_function_length": round(
                average_function_length, 2
            ),
            "maximum_function_length":
                maximum_function_length,
            "average_arguments": round(
                average_arguments, 2
            ),
            "maximum_arguments":
                maximum_arguments
        }