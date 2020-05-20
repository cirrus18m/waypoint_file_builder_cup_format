from easygui import fileopenbox #, filesavebox, msgbox, ccbox
import os
from copy import copy

class Remove_duplicates(object):
    def __init__(self, full_paths_of_sources=[], full_paths_of_target='result.cup'):
        """
        removes duplicated lines in waypoint files
        :param full_path_of_source: path to open source file (cup) - optional
        :output: writes converted file to disk
        """
        self.full_paths_of_sources = full_paths_of_sources
        self.lines_of_input = ['name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc\n']
        if len(self.full_paths_of_sources) == 0:
            self.full_paths_of_sources = fileopenbox(default=os.path.curdir, filetypes=["*.cup"])
            if self.full_paths_of_sources is None:
                print('Waypoint file loading was aborted by the user')
                quit()
        # load file:
        print(self.full_paths_of_sources)
        for full_path_of_source in self.full_paths_of_sources:
            print(full_path_of_source)
            print(self.load_cup_file(full_path_of_source))
            self.lines_of_input.extend(self.load_cup_file(full_path_of_source)[1::])  # do not attach header
        # remove duplicates
        self.lines_of_output = [self.lines_of_input[0]]
        self.lines_of_output.extend(sorted(self.lines_of_input[1::]))

        for idxLine in range(len(self.lines_of_output)-1,0,-1):  # backwards and one line less
            print(idxLine)
            line_cur = self.lines_of_output[idxLine]
            line_prev = self.lines_of_output[idxLine-1]
            # print(type(line_cur))
            splitted_cur = line_cur.split(',')
            splitted_prev = line_prev.split(',')
            # print(splitted_cur[0])
            # print(splitted_prev[0])
            removeLineFlag = False
            if splitted_cur[0] == splitted_prev[0]:
                removeLineFlag = True
            elif len(splitted_cur)<8:
                removeLineFlag = True
            elif not splitted_cur[6] in ['2','3','4','5','6']:
                # print(splitted_cur[6])
                removeLineFlag = True
            if removeLineFlag:
                # print('removing %s' % self.lines_of_output[idxLine])
                del self.lines_of_output[idxLine]
            else:  #  remove non value from frequency field
                newLine = copy(splitted_cur)
                if len(newLine[9])>8:
                    newLine[9] = newLine[9][0:8]
                    self.lines_of_output[idxLine] = ','.join(newLine)

        # export:
        print(self.lines_of_output[0])
        print('Input length was: %d & output length is: %d ' % (len(self.lines_of_input),len(self.lines_of_output)))
        self.write_cup_file(full_paths_of_target, self.lines_of_output)

    @staticmethod
    def load_cup_file(full_path):
        # read file
        print('reading file %s ' % full_path)
        f = open(full_path, 'r')  # add encoding here next time (manually converted o Ascci)
        lines = f.readlines()
        f.close()



        return lines

    @staticmethod
    def write_cup_file(full_path,lines):
        # read file
        print('writting file %s' % full_path)
        f = open(full_path, 'w')  # add encoding here next time (manually converted o Ascci)
        f.writelines(lines)
        f.close()



if __name__ == '__main__':
    filenamesAsList = ['ofm_CZ.cup','ofm_poland.cup','ofm_germany.cup']
    # filenamesAsList = ['result.cup']
    Remove_duplicates(filenamesAsList, 'result.cup')