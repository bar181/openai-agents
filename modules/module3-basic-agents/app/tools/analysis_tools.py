import re
import statistics
from typing import Dict, Any, List, Optional, Tuple, Pattern as RegexPattern, Match as RegexMatch
from pydantic import BaseModel
from app.tools.base_tool import BaseTool, ToolResult
from agents import function_tool


class SentimentResult(BaseModel):
    """Result of sentiment analysis."""
    score: float  # -1.0 to 1.0
    label: str  # "negative", "neutral", "positive"


class Entity(BaseModel):
    """Named entity extracted from text."""
    text: str
    type: str  # "person", "organization", "location", etc.
    start: int
    end: int


class Stats(BaseModel):
    """Basic statistical measures."""
    mean: float
    median: float
    mode: Optional[float] = None
    std_dev: float
    min: float
    max: float
    count: int


class Pattern(BaseModel):
    """Pattern found in data."""
    pattern_type: str  # "repetition", "sequence", "outlier", etc.
    description: str
    confidence: float  # 0.0 to 1.0


# Simple sentiment analysis using keyword matching
POSITIVE_WORDS = [
    "good", "great", "excellent", "amazing", "wonderful", "fantastic",
    "terrific", "outstanding", "superb", "brilliant", "awesome",
    "happy", "love", "best", "perfect", "positive"
]

NEGATIVE_WORDS = [
    "bad", "terrible", "awful", "horrible", "poor", "disappointing",
    "mediocre", "subpar", "worst", "hate", "dislike", "negative",
    "failure", "failed", "useless", "waste"
]


@function_tool
def analyze_sentiment(text: str) -> SentimentResult:
    """Analyzes text sentiment."""
    text_lower = text.lower()
    
    # Count positive and negative words
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    
    # Calculate sentiment score (-1.0 to 1.0)
    total = positive_count + negative_count
    if total == 0:
        score = 0.0
    else:
        score = (positive_count - negative_count) / total
    
    # Determine sentiment label
    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"
    
    return SentimentResult(score=score, label=label)


@function_tool
def extract_entities(text: str) -> List[Entity]:
    """Extracts named entities from text."""
    entities = []
    
    # Simple pattern matching for demonstration
    # Person pattern: Capitalized words
    person_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    for match in re.finditer(person_pattern, text):
        entities.append(Entity(
            text=match.group(),
            type="person",
            start=match.start(),
            end=match.end()
        ))
    
    # Organization pattern: All caps words
    org_pattern = r'\b[A-Z]{2,}\b'
    for match in re.finditer(org_pattern, text):
        entities.append(Entity(
            text=match.group(),
            type="organization",
            start=match.start(),
            end=match.end()
        ))
    
    # Location pattern: "in" followed by capitalized word
    loc_pattern = r'\bin ([A-Z][a-z]+)\b'
    for match in re.finditer(loc_pattern, text):
        entities.append(Entity(
            text=match.group(1),
            type="location",
            start=match.start(1),
            end=match.end(1)
        ))
    
    return entities


@function_tool
def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extracts key phrases from text."""
    # Simple implementation: split by spaces, filter out common words, take top N
    common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "of", "is", "are"}
    words = text.lower().split()
    filtered_words = [word for word in words if word not in common_words and len(word) > 3]
    
    # Count word frequencies
    word_counts = {}
    for word in filtered_words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Sort by frequency and take top N
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


@function_tool
def calculate_basic_stats(data: List[float]) -> Stats:
    """Calculates basic statistical measures."""
    if not data:
        raise ValueError("Data list cannot be empty")
    
    try:
        mean_val = statistics.mean(data)
        median_val = statistics.median(data)
        
        # Mode can fail if no unique mode exists
        try:
            mode_val = statistics.mode(data)
        except statistics.StatisticsError:
            mode_val = None
        
        std_dev = statistics.stdev(data) if len(data) > 1 else 0.0
        
        return Stats(
            mean=mean_val,
            median=median_val,
            mode=mode_val,
            std_dev=std_dev,
            min=min(data),
            max=max(data),
            count=len(data)
        )
    except Exception as e:
        raise ValueError(f"Error calculating statistics: {str(e)}")


@function_tool
def perform_correlation(x: List[float], y: List[float]) -> float:
    """Calculates correlation coefficient between two data series."""
    if len(x) != len(y):
        raise ValueError("Data series must have the same length")
    
    if len(x) < 2:
        raise ValueError("Data series must have at least 2 points")
    
    try:
        return statistics.correlation(x, y)
    except Exception as e:
        raise ValueError(f"Error calculating correlation: {str(e)}")


@function_tool
def find_patterns(data: List[Any]) -> List[Pattern]:
    """Identifies patterns in data."""
    patterns = []
    
    # Check for repetition
    if len(data) > 1:
        repeats = {}
        for item in data:
            item_str = str(item)
            repeats[item_str] = repeats.get(item_str, 0) + 1
        
        for item, count in repeats.items():
            if count > 1 and count / len(data) > 0.2:
                patterns.append(Pattern(
                    pattern_type="repetition",
                    description=f"Item '{item}' repeats {count} times",
                    confidence=min(count / len(data), 1.0)
                ))
    
    # Check for sequence (if numeric)
    if all(isinstance(x, (int, float)) for x in data) and len(data) > 2:
        diffs = [data[i+1] - data[i] for i in range(len(data)-1)]
        if len(set(diffs)) == 1:
            patterns.append(Pattern(
                pattern_type="sequence",
                description=f"Arithmetic sequence with difference {diffs[0]}",
                confidence=1.0
            ))
    
    # Check for outliers (if numeric)
    if all(isinstance(x, (int, float)) for x in data) and len(data) > 4:
        mean_val = statistics.mean(data)
        std_dev = statistics.stdev(data)
        
        for i, val in enumerate(data):
            z_score = abs(val - mean_val) / std_dev
            if z_score > 2.0:
                patterns.append(Pattern(
                    pattern_type="outlier",
                    description=f"Outlier at position {i}: value {val}",
                    confidence=min(z_score / 3.0, 1.0)
                ))
    
    return patterns


@function_tool
def apply_regex(text: str, pattern: str) -> List[Dict[str, Any]]:
    """Applies regex pattern to text."""
    try:
        compiled_pattern = re.compile(pattern)
        matches = []
        
        for match in compiled_pattern.finditer(text):
            match_dict = {
                "match": match.group(),
                "start": match.start(),
                "end": match.end(),
                "groups": {}
            }
            
            # Add named groups
            for name, value in match.groupdict().items():
                match_dict["groups"][name] = value
            
            # Add numbered groups
            for i, group in enumerate(match.groups(), 1):
                match_dict["groups"][str(i)] = group
            
            matches.append(match_dict)
        
        return matches
    
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {str(e)}")


class TextAnalysisTool(BaseTool):
    """Tool for text analysis operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation in ["sentiment", "entities", "keywords"]:
            return "text" in kwargs
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the text analysis tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "sentiment":
                result = analyze_sentiment(kwargs["text"])
                return ToolResult(success=True, data=result)
            
            elif operation == "entities":
                result = extract_entities(kwargs["text"])
                return ToolResult(success=True, data=result)
            
            elif operation == "keywords":
                max_keywords = kwargs.get("max_keywords", 5)
                result = extract_keywords(kwargs["text"], max_keywords)
                return ToolResult(success=True, data=result)
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing text analysis tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Analyzes text with operations like sentiment analysis, entity extraction, and keyword extraction. "
            "Operations: sentiment, entities, keywords."
        )


class StatisticsTool(BaseTool):
    """Tool for statistical analysis operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "basic_stats":
            return "data" in kwargs and isinstance(kwargs["data"], list)
        elif operation == "correlation":
            return ("x" in kwargs and isinstance(kwargs["x"], list) and
                    "y" in kwargs and isinstance(kwargs["y"], list))
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the statistics tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "basic_stats":
                result = calculate_basic_stats(kwargs["data"])
                return ToolResult(success=True, data=result)
            
            elif operation == "correlation":
                result = perform_correlation(kwargs["x"], kwargs["y"])
                return ToolResult(success=True, data={"correlation": result})
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing statistics tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Performs statistical analysis with operations like basic statistics and correlation. "
            "Operations: basic_stats, correlation."
        )


class PatternTool(BaseTool):
    """Tool for pattern analysis operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "find_patterns":
            return "data" in kwargs and isinstance(kwargs["data"], list)
        elif operation == "apply_regex":
            return ("text" in kwargs and isinstance(kwargs["text"], str) and
                    "pattern" in kwargs and isinstance(kwargs["pattern"], str))
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the pattern tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "find_patterns":
                result = find_patterns(kwargs["data"])
                return ToolResult(success=True, data=result)
            
            elif operation == "apply_regex":
                result = apply_regex(kwargs["text"], kwargs["pattern"])
                return ToolResult(success=True, data=result)
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing pattern tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Analyzes patterns in data with operations like pattern finding and regex application. "
            "Operations: find_patterns, apply_regex."
        )