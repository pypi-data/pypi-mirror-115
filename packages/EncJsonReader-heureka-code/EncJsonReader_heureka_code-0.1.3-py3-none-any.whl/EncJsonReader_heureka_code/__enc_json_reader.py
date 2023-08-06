import json
from os.path import abspath, isfile
from AESEncryptor_heureka_code import AESTextEncryptor
from AESEncryptor_heureka_code.Exceptions import PasswordError, TextError


class EncJsonReader:
    def __init__(self, file: str, passwort: str, signatur: str = None):
        self.__aes: AESTextEncryptor = AESTextEncryptor(passwort=passwort, signaturtext=signatur)
        self.__file = abspath(file)
        self.__content = {}

        self.__create_file_if_not_exists(self.__aes, self.file)
        self.read()
        pass

    def read(self):
        try:
            with open(self.file) as file:
                enc_content = file.read()
            content = self.__aes.decrypt(enc_content)
            self.__content = json.loads(content)
            if self.__content is None:
                self.__content = {}
        except json.JSONDecodeError:
            self.write()
            self.read()
        except PasswordError:
            self.write()
            self.read()
        except TextError:
            self.write()
            self.read()
        pass

    def write(self):
        with open(self.file, "w") as file:
            file.write(self.__aes.encrypt(json.dumps(self.__content, indent=4)))
        pass

    def set_from_path(self, path: str, value):
        aktuelles_dic = self.__content
        pfad = path.split("/")
        while len(pfad) > 0:
            try:
                if pfad[0] in aktuelles_dic.keys():
                    if aktuelles_dic[pfad[0]] in [list, dict]:
                        aktuelles_dic = aktuelles_dic[pfad[0]]
                else:
                    if len(pfad) == 1:
                        aktuelles_dic[pfad[0]] = value
                    else:
                        aktuelles_dic[pfad[0]] = {}
            except AttributeError:
                if len(aktuelles_dic) < int(pfad[0]):
                    if len(pfad) == 1:
                        aktuelles_dic[int(pfad[0])] = value
                    else:
                        aktuelles_dic[int(pfad[0])] = {}
                else:
                    aktuelles_dic.append(value)

            try:
                aktuelles_dic = aktuelles_dic[pfad[0]]
            except TypeError:
                aktuelles_dic = aktuelles_dic[int(pfad[0])]
            del pfad[0]
        self.write()
        pass

    def get_from_path(self, path: str):
        pfad = path.split("/")
        aktuelles_dic = self.__content
        while len(pfad) > 0:
            if len(pfad) == 0:
                break
            if type(aktuelles_dic) == list:
                try:
                    aktuelles_dic = aktuelles_dic[int(pfad[0])]
                except IndexError:
                    break
                except ValueError:
                    break
            elif type(aktuelles_dic) == dict:
                try:
                    aktuelles_dic = aktuelles_dic[pfad[0]]
                except KeyError:
                    break
            del pfad[0]
        return aktuelles_dic

    def delete_path(self, path: str):
        try:
            pfad = path.split("/")
            aktuelles_dic = self.__content

            try:
                while len(pfad) > 1:
                    assert pfad[0] in aktuelles_dic.keys()
                    aktuelles_dic = aktuelles_dic[pfad[0]]
                    del pfad[0]
            except KeyError:
                pass
            except AssertionError:
                pass

            try:
                del aktuelles_dic[pfad[0]]
            except TypeError:
                del aktuelles_dic[pfad[0]]

        except KeyError:
            pass
        self.write()
        pass

    def path_exists(self, path: str):
        """ Prueft, ob der gegebene Pfad existiert """
        if self.get_from_path(path) == self.__content:
            return path == ""
        return True

    @staticmethod
    def __create_file_if_not_exists(aes: AESTextEncryptor, filename: str):
        if isfile(filename) is False:
            with open(filename, "w") as file:
                file.write(aes.encrypt("{}"))
        pass

    @property
    def file(self) -> str:
        return self.__file

    @property
    def passwort(self) -> str:
        return self.__aes.passwort

    @property
    def signatur(self) -> str:
        return self.__aes.signaturtext

    def __copy__(self):
        return EncJsonReader(file=self.file, passwort=self.passwort, signatur=self.signatur)

    def __repr__(self):
        return f"<EncJsonReader file={self.file}>"
    pass
