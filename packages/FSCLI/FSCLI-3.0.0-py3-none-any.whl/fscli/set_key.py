import os

class SetKey:
    def __init__(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__)) + '/config.py'
        self.key: str = ''
    
    @staticmethod
    def get_key() -> str:
        key = input("Enter the API KEY: ")
        return key

    def append_key_in_file(self) -> None:
        with open(self.current_path, 'a') as f:
            f.write('\nAT_KEY = "{}"'.format(self.key))

    def return_key(self) -> str:
        return self.key
    
    def change_key(self):
        """
        Change the API key in the config file.
        """
        pass
        
    def main(self):
        self.key = self.get_key()
        self.append_key_in_file()

if __name__ == '__main__':
    SetKey().main()
