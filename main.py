import argparse
import subprocess
import re


def run_traceroute(target, progressive=False, output_file=None):
    """Execute a traceroute command and manage its output."""
    command = ["traceroute", target]

    # Expression pour fetch adresses ip
    ip_regex = r"\d+\.\d+\.\d+\.\d+"

    if progressive:
        # Affichage progressif des résultats
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if output_file:
            try:
                file = open(output_file, "w")
            except IOError as error:
                print(f"There was an error while opening the file \n Error: {error}")
        else:
            file = None

        for line in process.stdout:
            ips = re.findall(ip_regex, line)  # Trouver IP
            for ip in ips:
                print(ip)  # Afficher IP 
                if file:
                    file.write(ip + "\n")  # Écrire l'IP fichier
        process.wait()

        if file:
            file.close()

    else:
        # Résultat complet à la fin
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Traceroute did not execute properly : {result.stderr}")
            return
        output = result.stdout
        ips = re.findall(ip_regex, output)  # Trouver toutes les IPs dans la sortie

        if output_file:
            try:
                with open(output_file, "w") as file:
                    for ip in ips:
                        file.write(ip + "\n")  # Écrire IPs dans le fichier
            except IOError as error:
                print(f"There was an error while opening the file \n Error: {error}")

        for ip in ips:
            print(ip) 


def main():
    parser = argparse.ArgumentParser(description="Traceroute IP hops for a given target.")
    parser.add_argument("target")
    parser.add_argument("-p", "--progressive", action="store_true")
    parser.add_argument("-o", "--output-file", type=str)

    args = parser.parse_args()

    run_traceroute(target=args.target, progressive=args.progressive, output_file=args.output_file)


if __name__ == "__main__":
    main()
