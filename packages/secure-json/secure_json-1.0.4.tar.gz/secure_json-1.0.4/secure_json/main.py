import sys
import json
import base64


class Dict2Class(object):
    def __init__(self, my_dict):
        for key in my_dict:
            value = my_dict[key]
            if type(value) == dict:
                value = Dict2Class(value)
            setattr(self, key, value)

    def __getattr__(self, attrname):
        if attrname not in self:
            raise KeyError(attrname)
        return self[attrname]

    def __delattr__(self, attrname):
        del self[attrname]


class Settings(object):
    def __init__(self, file_name):

        self.path = file_name
        self.validate_string = 'FDCjVPClMKUw4F3U8KUwpRmwo1TwpbDqsK5wprCoMOnw592wp5gw6HDp8K5wp1nw5jClsKAwo1Vw6XDns'

        if len(sys.argv) < 2:
            input('The password was not detected. Pass the password as a startup argument or read help.\nPress ENTER to exit.')
            sys.exit()
        elif sys.argv[1] == 'decode' or sys.argv[1] == 'encode':
            input('At first argument must be password.\nPress ENTER to exit.')
            sys.exit()

        self.password = sys.argv[1]

        if sys.argv[1] == 'help':
            text = '''
    You need to use password to access data from your json.
    main.py <password> <command>

    Commands:
    1. encode:
            description:
                encode file and rewrite current
            example:
                main.py password encode
    2. decode:
            description:
                decode file and rewrite current
            example:
                main.py password decode
            '''
            print(text)
            sys.exit()

        if len(sys.argv) == 2:
            with open(self.path, 'r', encoding='utf8') as file:
                all_text = file.read()

            if len(all_text) == 0:
                print(f'File [{self.path}] is empty.')
                sys.exit()

            if all_text.find('\n') == -1:
                result = self.decode(all_text)
                if self.validate_string in result:
                    data = json.loads(result)
                else:
                    input('Password is incorrect. Please try again.\nPress ENTER to exit.')
                    sys.exit()
            else:
                data = json.loads(all_text)

            if 'validate_string' in data and data['validate_string'] == self.validate_string:
                del data['validate_string']

            data = Dict2Class(data)

            self.__dict__['data'] = data
            return

        elif sys.argv[2] == 'encode':
            with open(self.path, 'r', encoding='utf8') as file:
                all_text = file.read()

            if len(all_text) == 0:
                input(f'File [{self.path}] is empty.\nPress ENTER to exit')
                sys.exit()

            try:
                json_data = json.loads(all_text)
            except:
                input('Data was encoded earlier.\nPress ENTER to exit.')
                sys.exit()

            json_data['validate_string'] = self.validate_string

            all_text = json.dumps(json_data)

            result = self.encode(all_text)

            with open(self.path, 'w', encoding='utf8') as file:
                file.write(result)

            print('Success.')
            sys.exit()

        elif sys.argv[2] == 'decode':
            with open(self.path, 'r', encoding='utf8') as file:
                all_text = file.read()

            if len(all_text) == 0:
                input(f'File [{self.path}] is empty.\nPress ENTER to exit.')
                sys.exit()

            if all_text.find('{') != -1 or all_text.find('[') != -1:
                input('Data not encoded. Operation aborted.\nPress ENTER to exit.')
                sys.exit()

            result = self.decode(all_text)

            correct_password = False

            try:
                json_data = json.loads(result)
                if 'validate_string' in json_data and json_data['validate_string'] == self.validate_string:
                    correct_password = True
                    del json_data['validate_string']
                    result = json.dumps(json_data, ensure_ascii=False, indent='    ')
            except:
                correct_password = False

            if not correct_password:
                input('Password is incorrect. Please try again.\nPress ENTER to exit.')
                sys.exit()

            with open(self.path, 'w', encoding='utf8') as file:
                file.write(result)

            print('Success.')
            sys.exit()

    def encode(self, value_to_encrypt):
        enc = []
        for i in range(len(value_to_encrypt)):
            key_c = self.password[i % len(self.password)]
            enc_c = chr((ord(value_to_encrypt[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = self.password[i % len(self.password)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)


if __name__ == '__main__':
    settings = Settings('settings.json').data
    a=0