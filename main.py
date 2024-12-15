import argparse
import subprocess


def run_traceroute(target, progressive=False, output_file=None):
    """Execute a traceroute command and manage its output."""
    command = ["traceroute", target]
    
    if progressive:
        # results appear progressively
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if output_file:
            file = open(output_file, "w")
        else:
            file = None

        for line in process.stdout:
            print(line)
            if file:
                file.write(line)
        process.wait()
    
        if file:
            file.close()
    else:
        # results appear at the end + stored in file
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if output_file:
            with open(output_file, "w") as file:
                file.write(output)
        print(output)



def main():
    parser = argparse.ArgumentParser(description="Traceroute IP hops for a given target.")
    parser.add_argument("target")
    parser.add_argument("-p", "--progressive", action="store_true")
    parser.add_argument("-o", "--output-file", type=str)

    args = parser.parse_args()

    run_traceroute(target=args.target, progressive=args.progressive, output_file=args.output_file)


if __name__ == "__main__":
    main()
