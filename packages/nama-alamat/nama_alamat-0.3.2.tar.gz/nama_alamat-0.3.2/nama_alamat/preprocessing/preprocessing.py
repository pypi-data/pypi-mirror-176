"""Module for preprocessing Indonesia Name and Address.

Dictionary for preproccesing on dict_files folder. Roman library used
for converting roman number to arabic.
"""
# import library
from __future__ import annotations

import os
import re

import roman

# membuat dictionary untuk preprocessing nama dan alamat
dict_alamat = {}
dict_nama = {}

here = os.path.dirname(os.path.abspath(__file__))

# menambahkan tiap baris dari file txt ke dictionary
with open(os.path.join(here, "dict_files", "dict_alamat.txt")) as file:
    for line in file:
        key, value = line.replace("'", "").rstrip("\n").split(":")
        dict_alamat[key] = value

with open(os.path.join(here, "dict_files", "dict_nama.txt")) as file:
    for line in file:
        key, value = line.replace("'", "").rstrip("\n").split(":")
        dict_nama[key] = value


class Preprocessing:
    """Preprocessing class."""

    def __init__(self, tipe="alamat"):
        """Class initialization.

        Args:
            tipe (str, optional): valid value : 'alamat' for address or 'nama' for name.
            Defaults to 'alamat'.
        """
        self.tipe = tipe

    # standarisasi penulisan nama dan alamat
    def standardize(self, strings):
        """Standardize function.

        Args:
            strings (_type_): input string

        Returns:
            _type_: returning standarized string based on type (name or address)
        """
        tipe = self.tipe
        if tipe == "alamat":
            result = " ".join(dict_alamat.get(ele, ele) for ele in strings.split())
        else:
            result = re.sub(r"\s", "_", strings)
            for i, k in dict_nama.items():
                str_from = "(_|^)" + i + "(_|$)"
                str_to = "_" + k + "_"
                result = re.sub(str_from, str_to, result)
            result = re.sub("_", " ", result)
        return result

    def std_rt_rw(self, text):
        """Standardize RT and RW function.

        Args:
            strings (_type_): input string

        Returns:
            _type_: returning standarized RTxxx RWxxx string
        """
        try:
            # rt 001 rw 001
            if re.search(r"rt[\s\.](?:[\d]+) rw[\s\.](?:[\d]+)", text):
                temp_txt = re.sub(r"[^\w\s]", " ", text)
                temp_txt = (
                    re.search(r"rt[\s\.](?:[\d]+) rw[\s\.](?:[\d]+)", temp_txt)
                    .group(0)
                    .split(" ")
                )
                temp_txt = (
                    "rt"
                    + str(temp_txt[1]).zfill(3)
                    + " "
                    + "rw"
                    + str(temp_txt[3]).zfill(3)
                )
                result = re.sub(r"rt[\s\.](?:[\d]+) rw[\s\.](?:[\d]+)", temp_txt, text)
            else:
                result = text
            # rt/rw 001/001
            if re.search(r"rt\/rw (?:[\d]+)(?:[\/])(?:[\d]+)", result):
                temp_txt = (
                    re.search(r"rt\/rw (?:[\d]+)(?:[\/])(?:[\d]+)", result)
                    .group(0)
                    .split(" ")
                )
                temp_txt = (
                    "rt"
                    + temp_txt[1].split("/")[0].zfill(3)
                    + " "
                    + "rw"
                    + temp_txt[1].split("/")[1].zfill(3)
                )
                result = re.sub(r"rt\/rw (?:[\d]+)(?:[\/])(?:[\d]+)", temp_txt, result)
            else:
                result = result
            # rt 003/013
            if re.search(r"rt \d+/\d+", result):
                temp_txt = re.search(r"rt \d+/\d+", result).group(0).split(" ")
                temp_txt = (
                    "rt"
                    + re.sub(r"[^\d]", "", temp_txt[1].split("/")[0]).zfill(3)
                    + " "
                    + "rw"
                    + re.sub(r"[^\d]", "", temp_txt[1].split("/")[1]).zfill(3)
                )
                result = re.sub(r"rt.\d+/\d+", temp_txt, result)
            else:
                result = result
            # 008/012
            if re.search(r"\d\d\d/\d\d\d", result):
                temp_txt = re.search(r"\d\d\d/\d\d\d", result).group(0)
                temp_txt = (
                    "rt"
                    + temp_txt.split("/")[0].zfill(3)
                    + " "
                    + "rw"
                    + temp_txt.split("/")[1].zfill(3)
                )
                result = re.sub(r"\d\d\d/\d\d\d", temp_txt, result)
            else:
                result = result
            # rt.003/013
            if re.search(r"rt.\d+/\d+", result):
                temp_txt = re.search(r"rt.\d+/\d+", result).group(0).split("t")
                temp_txt = (
                    "rt"
                    + re.sub(r"[^\d]", "", temp_txt[1].split("/")[0]).zfill(3)
                    + " "
                    + "rw"
                    + re.sub(r"[^\d]", "", temp_txt[1].split("/")[1]).zfill(3)
                )
                result = re.sub(r"rt.\d+/\d+", temp_txt, result)
            else:
                result = result
            # rt003/rw013
            if re.search(r"rt\d+/rw\d+", result):
                temp_txt = re.search(r"rt\d+/rw\d+", result).group(0).split("/")
                temp_txt = (
                    "rt"
                    + re.sub(r"[^\d]", "", temp_txt[0]).zfill(3)
                    + " "
                    + "rw"
                    + re.sub(r"[^\d]", "", temp_txt[1]).zfill(3)
                )
                result = re.sub(r"rt\d+/rw\d+", temp_txt, result)
            else:
                result = result
            # rt001 rw001
            if re.search(r"rt\d+ rw\d+", result):
                temp_txt = re.search(r"rt\d+ rw\d+", result).group(0).split(" ")
                temp_txt = (
                    "rt"
                    + re.sub(r"[^\d]", "", temp_txt[0]).zfill(3)
                    + " "
                    + "rw"
                    + re.sub(r"[^\d]", "", temp_txt[1]).zfill(3)
                )
                result = re.sub(r"rt\d+ rw\d+", temp_txt, result)
            else:
                result = result
            # rt.003 rw. 013
            if re.search(r"rt(?:\.|\s|.\s)\d+(?: | |, )rw(?:\.|\s|.\s)\d+", result):
                temp_txt = (
                    re.search(r"rt(?:\.|\s|.\s)\d+(?: | |, )rw(?:\.|\s|.\s)\d+", result)
                    .group(0)
                    .split("rw")
                )
                temp_txt = (
                    "rt"
                    + str(re.sub(r"[^0-9]", "", temp_txt[0])).zfill(3)
                    + " "
                    + "rw"
                    + str(re.sub(r"[^0-9]", "", temp_txt[1])).zfill(3)
                )
                result = re.sub(
                    r"rt(?:\.|\s|.\s)\d+(?: | |, )rw(?:\.|\s|.\s)\d+", temp_txt, result
                )
            else:
                result = result

            return result
        except Exception:
            print(text)

    def preprocessing(self, strings):
        """Preprocessing function.

        Args:
            strings (_type_): input string

        Returns:
            _type_: return preprocessed string
        """
        tipe = self.tipe

        # kata-kata tidak berguna
        stopword = [
            "please specify",
            "hold mail",
            "kota administrasi",
            "kota adm",
            "holdmail",
            "dummy",
            "unknown",
            "middlename",
            "npwp",
            "qq",
            "sp_xplor",
            "null",
            "anonymous",
            "not_associate",
            "pt tmj",
            "untuk",
            "petugas",
            "rt000 rw000",
            " rt ",
            " rw ",
        ]

        if isinstance(strings, str):
            # lowercase
            result = strings.lower()
            # remove inside bracket
            # result = re.sub(r'\([^)]*\)', '', result)
            # remove return chars, brackets, non ascii chars etc
            result = re.sub(r"\\r|\\t|\\n|\(|\[|\]|\)|[^\x00-\x7f]", "", result)
            result = " ".join(result.split())
            # remove old style name
            if tipe == "nama":
                # remove number
                result = re.sub(r"\d+", "", result)
                # pattern d o d i
                if re.match(r"^(?:\w ){2,}[a-z]$", result):
                    result = "".join(result.split())
                # pattern j.a.y.a.
                if re.match(r"^(?:\w\.){2,}$", result):
                    result = re.sub(r"[^\w ]", " ", result)
                    result = "".join(result.split())
                # pattern a s e p s.h.
                if re.match(r"^(?:\w ){2,}(?:[a-z.,]){2,4}$", result):
                    splitted = result.rsplit(" ", 1)
                    result = "".join(splitted[0].split())
                # pattern a s e p sh ma msc
                if re.search(r"^(?:\w ){2,}(?:[a-z.,]){2,4} ", result):
                    temp = re.sub(r"^(?:\w ){2,}(?:[a-z.,])[, ]", "", result)
                    len_res = len(temp.split())
                    splitted = result.rsplit(" ", len_res)
                    result = "".join(splitted[0].split())
                    temp = ""
                    for i in range(len(splitted)):
                        if i > 0:
                            temp = temp + " " + splitted[i]
                    result = result + temp
                # pattern h ir r u d y
                if re.search(r"(?:^| )(?:\w ){3,}[a-z]$", result):
                    temp = re.sub(r"(?:^| )(?:\w ){2,}[a-z]$", "", result)
                    len_res = len(temp.split())
                    splitted = result.split(" ", len_res)
                    result = "".join(splitted[-1].split())
                    temp = ""
                    for i in range(len(splitted)):
                        if i < len(splitted) - 1:
                            temp = splitted[i] + " " + temp
                    result = temp + result
                # pattern ir ali wahid m b a
                if re.search(
                    r"(?:(?:^| )(?:\w ){3,})|(?:(?: )(?:\w ){2,}[a-z])", result
                ):
                    temp = re.sub(
                        r"(?:(?:^| )(?:\w ){3,})|(?:(?: )(?:\w ){2,}[a-z])", "", result
                    )
                    temp1 = result.replace(temp, "")
                    temp1 = " " + "".join(temp1.split()) + " "
                    result = re.sub(
                        r"(?:(?:^| )(?:\w ){3,})|(?:(?: )(?:\w ){2,}[a-z])",
                        temp1,
                        result,
                    )
                    result = result.strip()

                if re.search(r"(oe)|(tj)|(dj)", result):
                    # ejaaan j
                    result = re.sub(r"j", "y", result)
                    # ejaan oe
                    result = re.sub(r"oe", "u", result)
                    # ejaan TJ
                    result = re.sub(r"ty", "c", result)
                    # ejaan DJ
                    result = re.sub(r"dy", "j", result)

                # ejaan oe
                result = re.sub(r"oe", "u", result)
                # ejaan TJ
                result = re.sub(r"tj", "c", result)
                # ejaan DJ
                result = re.sub(r"dj", "j", result)

            if tipe == "alamat":
                # remove kodepos
                result = re.sub(r" \d\d\d\d\d", "", result)
                # std rt dan rw
                result = self.std_rt_rw(result)
                # remove punctuation
                result = re.sub(r"[^\w\s]", " ", result)
                # remove duplicated jawa barat jawa barat
                result = re.sub(r"(\w+ \w+) \1", r"\1", result)
                # roman to arabic
                pattern = re.compile(
                    r"(^(?=[MDCLXVI])M*(C[MD]|"
                    r"D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$)"
                )
                result = " ".join(
                    [
                        str(roman.fromRoman(x))
                        if re.match(
                            pattern,
                            x,
                        )
                        else x
                        for x in result.upper().split()
                    ]
                ).lower()

            # remove aphostrophe
            result = re.sub(r"\'", "", result)
            # remove punctuation
            result = re.sub(r"[^\w\s]", " ", result)
            # remove stopword
            for i in stopword:
                result = re.sub(i, "", result)
            # remove whitespace
            result = result.strip()
            # remove double space
            result = re.sub(r"\s+", " ", result)
            # standardize
            result = self.standardize(result)
            # remove whitespace
            result = result.strip()
            # remove double space
            result = re.sub(r"\s+", " ", result)

            if tipe == "nama":
                # hapus nama 1 kata diulang
                result = [x.strip() for x in result.split()]
                result = " ".join(list(dict.fromkeys(result)))

            return result
        else:
            return strings
