#file: my_portfolio/utils/date_utils.py

from datetime import date

def duration(start_date, end_date):
    """
        Calculate and format the duration between two dates as a human-readable string.
        
        Handles three scenarios:
        1. When start_date is not provided: returns "Under planning"
        2. When end_date is not provided: returns an ongoing status with start date
        3. When both dates are provided: returns duration in years, months, and days
        
        The duration is broken down into the largest possible units (years > months > days)
        and only non-zero units are included. Proper pluralization is applied.
        
        Args:
            start_date (datetime.date or None): The starting date
            end_date (datetime.date or None): The ending date (None indicates ongoing)
        
        Returns:
            str: A formatted string representing the duration or status
        
        Examples:
            >>> duration(None, None)
            'Under planning'
            
            >>> duration(date(2023, 1, 1), None)
            'Started: 1 January, 2023 and On going'
            
            >>> duration(date(2020, 1, 1), date(2023, 2, 15))
            '3 years, 1 month, 14 days'
    """
    
    
    if not start_date:
        return "Under planning"
    if not end_date:
        # As day formatting in windows and unix-like systems are different
        # we need to handle it separately 
        try:
            day = start_date.strftime('%#d')  # Windows fallback
        except ValueError:
            day = start_date.strftime('%-d')  # Unix-like systems

        return f"Started: {day} {start_date.strftime('%B, %Y')} and On going"
    
    if start_date == end_date:
        return "Less than a day"
    
    total_days = (end_date - start_date).days
    years, remaining = divmod(total_days, 365)
    months, days = divmod(remaining, 30)
    
    parts = []
    if years: parts.append(f"{years} year{'s' if years!=1 else ''}")
    if months: parts.append(f"{months} month{'s' if months!=1 else ''}")
    if days or not parts: parts.append(f"{days} day{'s' if days!=1 else ''}")
    
    return ", ".join(parts)