import platform

def add_to_hosts_file(ip_address, hostname):
    try:
        # Determine the hosts file path based on the operating system
        system = platform.system()
        if system == 'Windows':
            hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        elif system == 'Linux' or system == 'Darwin':
            hosts_path = '/etc/hosts'
        else:
            raise Exception(f'Unsupported operating system: {system}')

        # Open hosts file in append mode and add the entry
        with open(hosts_path, 'a') as file:
            file.write(f'{ip_address}\t{hostname}\n')
            print("Finished editing hosts file")

        print(f'Added {hostname} to hosts file.')
    except Exception as e:
        print(f'Error adding {hostname} to hosts file: {str(e)}')

# Example usage
if __name__ == '__main__':
    add_to_hosts_file('127.0.0.1', 'api.sintra.com')
