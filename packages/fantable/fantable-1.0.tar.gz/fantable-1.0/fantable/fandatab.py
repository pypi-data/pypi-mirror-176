""" Simple dulu om, lain waktu update lagi """

class Table:
    def __init__(self, title=None):
        self.title = title
        self.__num = 0
        self.__tabl = {"coll": None, "trow": {}}
        self.__myTable = None

    def column(self, *arg):
        self.__tabl.update({"coll": [data for data in arg]})

    def tab_row(self, *arg):
        self.__num += 1
        self.__tabl["trow"].update({f"row{self.__num}": [data for data in arg]})

    def commit(self):
        for key, value in self.__tabl["trow"].items():
            if len(value) != len(self.__tabl["coll"]):
                exit("Error: The number of rows must equal the number of columns!")

        data_size = []
        spc, line, head = " ", "-", "="
        for i in range(len(self.__tabl["coll"])):
            data_temp = [self.__tabl["coll"][i]]
            for z in range(len(self.__tabl["trow"])):
                data_temp.append(self.__tabl["trow"][f"row{z+1}"][i])
            data_len = sorted(data_temp, key=len)
            data_size.append(len(data_len[-1]))
        head_line = "+" + "+".join(head * (d + 2) for d in data_size) + "+"
        row_line = "+" + "+".join(line * (d + 2) for d in data_size) + "+"
        pr_table = (
            "| "
            + " | ".join(
                f"{d[1]}{spc*(data_size[d[0]]-len(d[1]))}"
                for d in enumerate(self.__tabl["coll"])
            )
            + " |"
        )
        pr_table = f"{head_line}\n{pr_table}\n{head_line}"
        for key, value in self.__tabl["trow"].items():
            pr_tab = (
                "| "
                + " | ".join(
                    f"{d[1]}{spc*(data_size[d[0]]-len(d[1]))}" for d in enumerate(value)
                )
                + " |"
            )
            pr_table = f"{pr_table}\n{pr_tab}\n{row_line}"
        pr_table = pr_table if self.title is None else f"{spc*((len(head_line)-len(self.title))//2)}{self.title}\n{pr_table}"
        self.__myTable = pr_table

    def __str__(self):
        return str(self.__myTable)
