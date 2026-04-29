import argparse


def main():
    parser = argparse.ArgumentParser(prog='crypto_tracker', description='Crypto paper trading tracker (simulated)')
    sub = parser.add_subparsers(dest='command')

    exec_p = sub.add_parser('execute', help='Load trades from a model run')
    exec_p.add_argument('--run-id', required=True, help='Run ID from runs/ directory')

    sub.add_parser('watch', help='Start 24/7 price watcher (fills simulated orders)')

    sub.add_parser('monitor', help='Check expiries and show positions')

    report_p = sub.add_parser('report', help='Accuracy dashboard')
    report_p.add_argument('--last', type=int, default=7, help='Days to look back')
    report_p.add_argument('--mode', choices=['swing', 'daytrade'], help='Filter by mode')

    sub.add_parser('status', help='Show open positions')

    sub.add_parser('cash', help='Show available capital')

    args = parser.parse_args()

    if args.command == 'execute':
        from crypto_tracker.executor import execute_run
        execute_run(args.run_id)
    elif args.command == 'watch':
        from crypto_tracker.price_watcher import run_watcher
        run_watcher()
    elif args.command == 'monitor':
        from crypto_tracker.monitor import monitor_positions
        monitor_positions()
    elif args.command == 'report':
        from crypto_tracker.reporter import report
        report(days=args.last, mode=args.mode)
    elif args.command == 'status':
        from crypto_tracker.monitor import show_status
        show_status()
    elif args.command == 'cash':
        from crypto_tracker.db import get_available_cash
        print(f"Available cash: ${get_available_cash():,.2f}")
    else:
        parser.print_help()
