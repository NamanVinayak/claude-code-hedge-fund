import argparse


def main():
    parser = argparse.ArgumentParser(prog='tracker', description='Paper trading tracker')
    sub = parser.add_subparsers(dest='command')

    exec_p = sub.add_parser('execute', help='Place orders from a model run')
    exec_p.add_argument('--run-id', required=True, help='Run ID from runs/ directory')

    sub.add_parser('monitor', help='Check fills and manage positions')

    report_p = sub.add_parser('report', help='Accuracy dashboard')
    report_p.add_argument('--last', type=int, default=7, help='Days to look back')
    report_p.add_argument('--mode', choices=['swing', 'daytrade'], help='Filter by mode')

    sub.add_parser('status', help='Show open positions')

    sub.add_parser('cash', help='Show available cash (global)')

    sub.add_parser('budget', help='Show per-mode budget and deployment')

    sub.add_parser('watch', help='Watch prices and trigger entries for pending trades')

    args = parser.parse_args()

    if args.command == 'execute':
        from tracker.executor import execute_run
        execute_run(args.run_id)
    elif args.command == 'monitor':
        from tracker.monitor import monitor_positions
        monitor_positions()
    elif args.command == 'report':
        from tracker.reporter import report
        report(days=args.last, mode=args.mode)
    elif args.command == 'status':
        from tracker.monitor import show_status
        show_status()
    elif args.command == 'cash':
        from tracker.db import get_available_cash
        print(f"Available cash: ${get_available_cash():,.2f}")
    elif args.command == 'budget':
        import json, os
        from tracker.db import get_available_cash_for_mode, get_session, Trade
        watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')
        with open(watchlist_path) as f:
            config = json.load(f)
        settings = config['settings']
        session = get_session()
        for m in ('swing', 'daytrade'):
            budget_key = f'{m}_budget'
            budget = settings.get(budget_key, settings.get('paper_account_size', 5000))
            available = get_available_cash_for_mode(m)
            deployed = budget - available
            open_count = session.query(Trade).filter(
                Trade.mode == m,
                Trade.status.in_(['pending', 'entered'])
            ).count()
            label = m.upper()
            print(f"{label:9s}: ${available:>8,.2f} available of ${budget:>8,.2f}  ({open_count} open positions, ${deployed:>8,.2f} deployed)")
        session.close()
    elif args.command == 'watch':
        from tracker.price_watcher import run_watcher
        run_watcher()
    else:
        parser.print_help()
