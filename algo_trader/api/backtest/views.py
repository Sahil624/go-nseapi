# -*- coding: utf-8 -*-
"""User views."""
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import joinedload

from api.backtest.model import Backtest, BacktestIteration
from api.backtest.utils import list_strategy_files, load_strategy_class
from backtest import run_backtest
from api.database import db
blueprint = Blueprint("backtest", __name__, url_prefix="/backtest", static_folder="../static")


@blueprint.get("/iterations/")
@jwt_required()
def get_backtest_iterations():
    backtest_id = request.args.get('backtest_id')
    # Perform a single query to fetch all iterations for a given backtest_id
    iterations = db.session.query(BacktestIteration).filter(BacktestIteration.backtest_id == backtest_id).all()

    result = []
    for iteration in iterations:
        result.append({
            "id": iteration.id,
            "backtest_id": iteration.backtest_id,
            "symbol": iteration.symbol,
            "entry_date": iteration.entry_date,
            "entry_price": iteration.entry_price,
            "exit_date": iteration.exit_date,
            "exit_price": iteration.exit_price,
            "size": iteration.size,
            "direction": iteration.direction,
            "profit": iteration.profit,
            "commission": iteration.commission,
            "duration": iteration.duration
        })

    return jsonify(result), 200

@blueprint.get("/strategies")
@jwt_required()
def list_strategies():
    strategies_directory = 'strategies'
    strategy_files = list_strategy_files(strategies_directory)
    strategies = []
    for file in strategy_files:
        strategy_name = os.path.splitext(os.path.basename(file))[0]
        strategy_class = load_strategy_class(strategy_name)
        if strategy_class and strategy_class.params.is_enabled:
            strategies.append({'strategy_code': os.path.splitext(os.path.basename(file))[0] ,**strategy_class.get_metadata()})
    return jsonify({"strategies": strategies})


@blueprint.get("/")
@jwt_required()
def get_backtests():
    user_id = get_jwt_identity()

    # Perform a single query using joinedload to fetch backtests and their analysis
    backtests = db.session.query(Backtest).options(joinedload(Backtest.analysis)).filter(Backtest.user_id == user_id).all()
    
    result = []
    for backtest in backtests:
        # analysis = backtest.analysis.first() if backtest.analysis else None
        result.append({
            "id": backtest.id,
            "strategy": backtest.strategy,
            "symbol": backtest.symbol,
            "from_date": backtest.from_date,
            "to_date": backtest.to_date,
            "created_at": backtest.created_at,
            "analysis": backtest.analysis.result if backtest.analysis else None
        })

    return jsonify(result), 200

@blueprint.post("/")
@jwt_required()
def backtest():   
    data = request.json
    strategy_name = data['strategy']
    symbol = data['symbol']
    from_date = data['from_date']
    to_date = data['to_date']

    strategy_class = load_strategy_class(strategy_name)
    
    if strategy_class is None:
        return jsonify({"error": "Strategy not found"}), 404

    backtest, stats = run_backtest(strategy_class, symbol, from_date, to_date)
    return jsonify({"backtest_id": backtest.id, "result": stats})
