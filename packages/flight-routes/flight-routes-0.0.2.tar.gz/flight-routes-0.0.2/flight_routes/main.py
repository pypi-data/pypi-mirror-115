import argparse

from flight_routes import flight_plan_searcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='kiwi flight search', epilog="autor: Bc. Filip Agh")
    parser.add_argument('csvPath', type=str)
    parser.add_argument('origin', type=str)
    parser.add_argument('destination', type=str)
    parser.add_argument('--bags', type=int)
    parser.add_argument('--return', dest="ret", action='store_true')
    parser.set_defaults(ret=False, bags=0)
    args = parser.parse_args()

    json_result = flight_plan_searcher.search(args.csvPath, args.origin, args.destination, args.bags, args.ret)

    print(json_result)
