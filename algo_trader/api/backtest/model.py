from api.database import PkModel, db


class Backtest(PkModel):
    __tablename__ = "backtest"
    strategy = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    from_date = db.Column(db.String(10), nullable=False)
    to_date = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.current_timestamp())
    analysis = db.relationship('Analysis', back_populates='backtest', uselist=False, cascade="all, delete-orphan")


class Analysis(PkModel):
    backtest_id = db.Column(db.String(36), db.ForeignKey('backtest.id'), nullable=False)
    result = db.Column(db.Text, nullable=False)
    backtest = db.relationship('Backtest', back_populates='analysis')

class BacktestIteration(PkModel):
    __tablename__ = "backtest_iterations"
    backtest_id = db.Column(db.String(36), db.ForeignKey('backtest.id'), nullable=False)
    symbol = db.Column(db.String(20))
    entry_date = db.Column(db.Date)
    entry_price = db.Column(db.Float)
    exit_date = db.Column(db.Date)
    exit_price = db.Column(db.Float)
    size = db.Column(db.Integer)
    direction = db.Column(db.String)
    profit = db.Column(db.Float)
    commission = db.Column(db.Float)
    duration = db.Column(db.Integer)

    # backtest = db.relationship("Backtest", back_populates="backtest_iterations")