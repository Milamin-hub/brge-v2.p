class Color:
    def __green(self, text, after=''):
        text = str(text)
        after = str(after)
        return "\033[92m\033[1m" + text + "\033[0m" + ' ' + after
    
    def __yellow(self, text, after=''):
        text = str(text)
        after = str(after)
        return "\033[93m\033[1m" + text + "\033[0m" + ' ' + after

    def __red(self, text, after=''):
        text = str(text)
        after = str(after)
        return "\033[91m\033[1m" + text + "\033[0m" + ' ' + after
  
    def __white(self, text, after=''):
        text = str(text)
        after = str(after)
        return "\033[1m" + text + "\033[0m" + ' ' + after
    
    def __blue(self, text, after=''):
        text = str(text)
        after = str(after)
        return "\033[94m\033[1m" + text + "\033[0m" + ' ' + after
    
    def log_ok(self, text, after=''):
        print(self.__green(text, after))
    
    def log_er(self, text, after=''):
        print(self.__red(text, after))

    def log_warn(self, text, after=''):
        print(self.__yellow(text, after))

    def log_some(self, text, after=''):
        print(self.__blue(text, after))

    def log(self, text, after=''):
        print(self.__white(text, after))
        

c = Color()

logOk = lambda text, after='': c.log_ok(text, after)
logEr = lambda text, after='': c.log_er(text, after)
logW = lambda text, after='': c.log_warn(text, after)
logBlue = lambda text, after='': c.log_some(text, after)
log = lambda text, after='': c.log(text, after)

