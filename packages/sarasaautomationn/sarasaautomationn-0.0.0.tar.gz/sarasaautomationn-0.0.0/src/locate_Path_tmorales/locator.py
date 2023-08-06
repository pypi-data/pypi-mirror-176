import os
import sys


class LocatorClass:
    def __init__(self, repo_name):
        self.__entire_disk = os.getcwd()
        self.__repo_name = repo_name
        self.__new_path = ''

    def locator_searcher(self):
        if not self.__repo_name.isdigit():

            # si ejecuto el test desde cualquier posicion de cmd, y si no le paso custom params
            if not bool(self.__entire_disk.__contains__(self.__repo_name)) and len(sys.argv) == 1:
                arg_path = sys.argv[0]
                directories = arg_path.split('\\')

                for directory in directories:
                    if directory == self.__repo_name:
                        return sys.path.append(self.__new_path[1:])
                    else:
                        self.__new_path = self.__new_path + '\\' + directory

            # si digo especifocamente la ruta del repo un nivel arriba
            elif len(sys.argv) > 2 and sys.argv[1] == '--custom-path':
                custom_path = sys.argv[2]
                sys.path.append(custom_path)

            # si el disco donde estoy parado no tiene el repo ej: C:\automation
            elif self.__entire_disk[:13] != self.__entire_disk[:3] + self.__repo_name:
                directories = self.__entire_disk.split('\\')

                for directory in directories:
                    if directory == self.__repo_name:
                        return sys.path.append(self.__new_path[1:])
                    else:
                        self.__new_path = self.__new_path + '\\' + directory

            # por descarte el repo esta al lado del disco, C:\automation
            else:
                return sys.path.append(self.__entire_disk[0:3])
        else:
            raise TypeError("The param for LocatorClass.__init__(self, repo_name) must be 'string'")
