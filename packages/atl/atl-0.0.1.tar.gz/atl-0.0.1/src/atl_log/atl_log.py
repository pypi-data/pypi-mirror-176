class AtlLogColor:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    
__atl_log_enable = False

def atl_log_enable() -> None:
  global __atl_log_enable
  __atl_log_enable = True
  
def atl_log_disable() -> None:
  global __atl_log_enable
  __atl_log_enable = False
  
def atl_log(msg: str, color: AtlLogColor = AtlLogColor.ENDC) -> None:
  if(color != AtlLogColor.ENDC):
    print(f'{color}[LOG] {msg}{AtlLogColor.ENDC}')
  else:
    print(f'[LOG] {msg}')
    
if __name__ == '__main__':
  atl_log_enable()
  atl_log('Hello', AtlLogColor.WARNING)
  atl_log('Bye')