"""
Trace processor for logging and monitoring agent interactions.

This module contains classes and functions for implementing tracing capabilities
to track agent actions, guardrail activations, and handoffs.
"""

import logging
import json
import time
from typing import Dict, Any, List, Optional
from agents.tracing import add_trace_processor, get_current_trace
from app import config

logger = logging.getLogger(__name__)

class OrchestrationTraceProcessor:
    """
    Custom trace processor for orchestration operations.
    
    This processor captures and processes trace data from agents, guardrails, and handoffs.
    """
    
    def __init__(self, log_level: str = config.TRACE_LOG_LEVEL):
        """Initialize the trace processor with the specified log level."""
        self.log_level = log_level
        self.traces: Dict[str, Dict[str, Any]] = {}
        logger.info(f"Initialized OrchestrationTraceProcessor with log level: {log_level}")
    
    def on_trace_start(self, trace):
        """Called when a trace starts."""
        logger.info(f"Trace started: {trace.trace_id}")
    
    def on_trace_end(self, trace):
        """Called when a trace ends."""
        logger.info(f"Trace ended: {trace.trace_id}")
        self.process_trace(trace)
    
    def on_span_start(self, span):
        """Called when a span starts."""
        # Use span_id instead of name for SpanImpl objects
        span_id = getattr(span, "span_id", "unknown")
        logger.info(f"Span started: {span_id}")
    
    def on_span_end(self, span):
        """Called when a span ends."""
        # Use span_id instead of name for SpanImpl objects
        span_id = getattr(span, "span_id", "unknown")
        logger.info(f"Span ended: {span_id}")
        
    def process_trace(self, trace):
        """
        Process a trace from an agent operation.
        
        Args:
            trace: The trace to process.
        """
        trace_id = trace.trace_id
        
        # Get attributes safely with getattr to handle different trace implementations
        start_time = getattr(trace, "start_time", time.time())
        end_time = getattr(trace, "end_time", time.time())
        spans = getattr(trace, "spans", [])
        metadata = getattr(trace, "metadata", {})
        
        # Store the trace
        self.traces[trace_id] = {
            "trace_id": trace_id,
            "start_time": start_time,
            "end_time": end_time,
            "duration_ms": (end_time - start_time) * 1000,
            "spans": [self._process_span(span) for span in spans],
            "metadata": metadata
        }
        
        # Log the trace
        logger.log(
            getattr(logging, self.log_level),
            f"Trace {trace_id}: {json.dumps(self.traces[trace_id], indent=2)}"
        )
    
    def _process_span(self, span) -> Dict[str, Any]:
        """
        Process a span from a trace.
        
        Args:
            span: The span to process.
            
        Returns:
            A dictionary representation of the span.
        """
        # Get attributes safely with getattr to handle different span implementations
        span_id = getattr(span, "span_id", "unknown")
        parent_id = getattr(span, "parent_id", None)
        name = getattr(span, "name", "unknown")
        start_time = getattr(span, "start_time", time.time())
        end_time = getattr(span, "end_time", time.time())
        attributes = getattr(span, "attributes", {})
        
        return {
            "span_id": span_id,
            "parent_id": parent_id,
            "name": name,
            "start_time": start_time,
            "end_time": end_time,
            "duration_ms": (end_time - start_time) * 1000,
            "attributes": attributes
        }
    
    def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a trace by its ID.
        
        Args:
            trace_id: The ID of the trace to get.
            
        Returns:
            The trace, or None if not found.
        """
        return self.traces.get(trace_id)
    
    def get_all_traces(self) -> List[Dict[str, Any]]:
        """
        Get all traces.
        
        Returns:
            A list of all traces.
        """
        return list(self.traces.values())
    
    def clear_traces(self) -> None:
        """Clear all traces."""
        self.traces.clear()
        logger.info("All traces cleared")

    def get_trace_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all traces.
        
        Returns:
            A summary of all traces.
        """
        if not self.traces:
            return {"count": 0, "message": "No traces available"}
        
        total_duration = sum(trace["duration_ms"] for trace in self.traces.values())
        avg_duration = total_duration / len(self.traces)
        
        return {
            "count": len(self.traces),
            "total_duration_ms": total_duration,
            "avg_duration_ms": avg_duration,
            "trace_ids": list(self.traces.keys())
        }
    
    def shutdown(self) -> None:
        """
        Shutdown the trace processor.
        
        This method is called when the application is shutting down.
        It performs any necessary cleanup operations.
        """
        logger.info("Shutting down OrchestrationTraceProcessor")
        self.clear_traces()

# Create a singleton instance of the trace processor
trace_processor = OrchestrationTraceProcessor()

# Register the trace processor with the agents library
add_trace_processor(trace_processor)

def format_trace_for_display(trace: Dict[str, Any]) -> str:
    """
    Format a trace for display in a hierarchical format.
    
    Args:
        trace: The trace to format.
        
    Returns:
        A formatted string representation of the trace.
    """
    output = []
    
    # Add trace header
    output.append(f"Trace ID: {trace['trace_id']}")
    output.append(f"Duration: {trace['duration_ms']:.2f} ms")
    output.append(f"Start Time: {trace['start_time']}")
    output.append(f"End Time: {trace['end_time']}")
    output.append("")
    
    # Add spans in a hierarchical format
    spans_by_id = {span["span_id"]: span for span in trace["spans"]}
    root_spans = [span for span in trace["spans"] if not span["parent_id"]]
    
    for root_span in root_spans:
        _format_span(root_span, spans_by_id, output, indent=0)
    
    return "\n".join(output)

def _format_span(span: Dict[str, Any], spans_by_id: Dict[str, Dict[str, Any]], output: List[str], indent: int) -> None:
    """
    Format a span and its children recursively.
    
    Args:
        span: The span to format.
        spans_by_id: A dictionary mapping span IDs to spans.
        output: The output list to append to.
        indent: The current indentation level.
    """
    # Add span header
    output.append(f"{' ' * indent}|- {span['name']} ({span['duration_ms']:.2f} ms)")
    
    # Add span attributes
    for key, value in span["attributes"].items():
        output.append(f"{' ' * (indent + 3)}|- {key}: {value}")
    
    # Add child spans
    child_spans = [s for s in spans_by_id.values() if s["parent_id"] == span["span_id"]]
    for child_span in child_spans:
        _format_span(child_span, spans_by_id, output, indent + 3)