"""
Usage tracking model.
"""
from datetime import datetime

from app import db


class UsageLog(db.Model):
    """Log of API requests for usage tracking."""
    
    __tablename__ = 'usage_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    api_key_id = db.Column(db.Integer, nullable=True, index=True)  # Optional for Zero-Gate
    
    # Request info
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    response_time_ms = db.Column(db.Integer, nullable=True)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<UsageLog {self.endpoint} @ {self.timestamp}>'
    
    @classmethod
    def log_request(cls, api_key_id: int, endpoint: str, method: str, status_code: int, response_time_ms: int = None):
        """Log an API request."""
        log = cls(
            api_key_id=api_key_id,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time_ms=response_time_ms
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    @classmethod
    def get_usage_stats(cls, api_key_id: int, days: int = 30):
        """Get usage statistics for an API key."""
        from datetime import timedelta
        from sqlalchemy import func
        
        since = datetime.utcnow() - timedelta(days=days)
        
        total = cls.query.filter(
            cls.api_key_id == api_key_id,
            cls.timestamp >= since
        ).count()
        
        by_endpoint = db.session.query(
            cls.endpoint,
            func.count(cls.id).label('count')
        ).filter(
            cls.api_key_id == api_key_id,
            cls.timestamp >= since
        ).group_by(cls.endpoint).all()
        
        by_day = db.session.query(
            func.date(cls.timestamp).label('date'),
            func.count(cls.id).label('count')
        ).filter(
            cls.api_key_id == api_key_id,
            cls.timestamp >= since
        ).group_by(func.date(cls.timestamp)).all()
        
        return {
            'total_requests': total,
            'by_endpoint': [{'endpoint': e, 'count': c} for e, c in by_endpoint],
            'by_day': [{'date': str(d), 'count': c} for d, c in by_day]
        }
