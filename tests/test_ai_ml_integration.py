"""
Comprehensive integration tests for AI/ML features
اختبارات تكاملية شاملة لميزات الذكاء الاصطناعي وتعليم الآلة
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

import pytest
from bayan import HybridLexer, HybridParser, HybridInterpreter


def test_neural_network_layer_with_varargs():
    """Test neural network layer implementation using *args and **kwargs"""
    code = """
class NeuralLayer:
{
    def __init__(self, *weights, **config):
    {
        self.weights = weights
        self.config = config
        self.activation = "sigmoid"
    }
    
    def forward(self, input1, input2, input3):
    {
        # Simple weighted sum
        total = input1 * 0.5 + input2 * 0.3 + input3 * 0.2
        return total
    }
}

# Create layer with weights and config
layer = NeuralLayer(0.5, 0.3, 0.2, activation="sigmoid", learning_rate=0.01)

# Forward pass
output = layer.forward(1.0, 2.0, 3.0)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)
    
    # Check that the layer was created and forward pass worked
    layer = interpreter.traditional.global_env['layer']
    # weights is a tuple from *args
    assert layer.attributes['weights'] == (0.5, 0.3, 0.2)
    # config is a dict from **kwargs
    config = layer.attributes['config']
    assert config['activation'] == 'sigmoid'
    assert config['learning_rate'] == 0.01
    
    output = interpreter.traditional.global_env['output']
    # 1.0*0.5 + 2.0*0.3 + 3.0*0.2 = 0.5 + 0.6 + 0.6 = 1.7
    assert abs(output - 1.7) < 0.001


def test_data_processing_with_builtins():
    """Test data processing using built-in functions"""
    code = """
# Sample dataset
data = [10, 25, 15, 30, 20]

# Statistical analysis
total = sum(data)
minimum = min(data)
maximum = max(data)
sorted_data = sorted(data)

# Check if all positive
all_positive = True
for val in data:
{
    if val <= 0:
    {
        all_positive = False
    }
}

# Check if any large
any_large = False
for val in data:
{
    if val > 25:
    {
        any_large = True
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Check results
    assert interpreter.traditional.global_env['total'] == 100
    assert interpreter.traditional.global_env['minimum'] == 10
    assert interpreter.traditional.global_env['maximum'] == 30
    assert interpreter.traditional.global_env['sorted_data'] == [10, 15, 20, 25, 30]
    assert interpreter.traditional.global_env['all_positive'] == True
    assert interpreter.traditional.global_env['any_large'] == True


def test_expert_system_with_dynamic_kb():
    """Test expert system with dynamic knowledge base using direct API"""
    from bayan.logical_engine import LogicalEngine, Fact, Rule, Predicate, Term

    engine = LogicalEngine()

    # Add symptoms for patient1
    engine.add_fact(Fact(Predicate('symptom', [Term('patient1'), Term('fever')])))
    engine.add_fact(Fact(Predicate('symptom', [Term('patient1'), Term('cough')])))

    # Add diagnosis rule for flu
    head1 = Predicate('diagnosis', [Term('X', is_variable=True), Term('flu')])
    body1 = [
        Predicate('symptom', [Term('X', is_variable=True), Term('fever')]),
        Predicate('symptom', [Term('X', is_variable=True), Term('cough')])
    ]
    engine.add_rule(Rule(head1, body1))

    # Query for patient1 diagnosis
    goal1 = Predicate('diagnosis', [Term('patient1'), Term('D', is_variable=True)])
    result1 = engine.query(goal1)
    assert len(result1) == 1
    assert result1[0].bindings['D'].value == 'flu'

    # Now add a new patient dynamically using assertz
    new_symptom = Fact(Predicate('symptom', [Term('patient3'), Term('fever')]))
    engine.assertz(new_symptom)
    new_symptom2 = Fact(Predicate('symptom', [Term('patient3'), Term('cough')]))
    engine.assertz(new_symptom2)

    # Query for patient3 diagnosis
    goal3 = Predicate('diagnosis', [Term('patient3'), Term('D', is_variable=True)])
    result3 = engine.query(goal3)

    # Patient3 should be diagnosed with flu
    assert len(result3) == 1
    assert result3[0].bindings['D'].value == 'flu'


def test_data_collection_with_bagof_setof():
    """Test data collection and analysis using bagof/setof with direct API"""
    from bayan.logical_engine import LogicalEngine, Fact, Predicate, Term

    engine = LogicalEngine()

    # Add training data
    engine.add_fact(Fact(Predicate('training_sample', [Term(1), Term('class_a'), Term(0.8)])))
    engine.add_fact(Fact(Predicate('training_sample', [Term(2), Term('class_a'), Term(0.9)])))
    engine.add_fact(Fact(Predicate('training_sample', [Term(3), Term('class_b'), Term(0.3)])))
    engine.add_fact(Fact(Predicate('training_sample', [Term(4), Term('class_b'), Term(0.2)])))
    engine.add_fact(Fact(Predicate('training_sample', [Term(5), Term('class_a'), Term(0.85)])))

    # Collect all samples for class_a using bagof
    goal = Predicate('bagof', [
        Term('Score', is_variable=True),
        Predicate('training_sample', [Term('ID', is_variable=True), Term('class_a'), Term('Score', is_variable=True)]),
        Term('Scores', is_variable=True)
    ])
    result = engine.query(goal)

    # Should have 1 solution with list of scores
    assert len(result) == 1
    scores = result[0].bindings['Scores']
    assert len(scores) == 3
    assert 0.8 in scores
    assert 0.9 in scores
    assert 0.85 in scores

    # Now test setof for unique classes
    goal2 = Predicate('setof', [
        Term('Class', is_variable=True),
        Predicate('training_sample', [Term('ID', is_variable=True), Term('Class', is_variable=True), Term('Score', is_variable=True)]),
        Term('Classes', is_variable=True)
    ])
    result2 = engine.query(goal2)

    # Should have 1 solution with sorted unique classes
    assert len(result2) == 1
    classes = result2[0].bindings['Classes']
    assert classes == ['class_a', 'class_b']


def test_ml_pipeline_integration():
    """Test complete ML pipeline with all features"""
    code = """
class DataProcessor:
{
    def __init__(self, *features, **params):
    {
        self.features = features
        self.params = params
    }
    
    def process(self, data):
    {
        # Normalize data
        max_val = max(data)
        min_val = min(data)
        range_val = max_val - min_val
        
        normalized = []
        for val in data:
        {
            norm_val = (val - min_val) / range_val
            normalized.append(norm_val)
        }
        
        return normalized
    }
    
    def aggregate(self, data):
    {
        return sum(data) / len(data)
    }
}

# Create processor
processor = DataProcessor("age", "height", "weight", method="minmax")

# Process data
raw_data = [10, 20, 30, 40, 50]
processed = processor.process(raw_data)
average = processor.aggregate(processed)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)
    
    # Check processor
    processor = interpreter.traditional.global_env['processor']
    assert len(processor.attributes['features']) == 3
    params = processor.attributes['params']
    assert params['method'] == 'minmax'
    
    # Check processed data (should be normalized to [0, 0.25, 0.5, 0.75, 1.0])
    processed = interpreter.traditional.global_env['processed']
    assert abs(processed[0] - 0.0) < 0.001
    assert abs(processed[1] - 0.25) < 0.001
    assert abs(processed[2] - 0.5) < 0.001
    assert abs(processed[3] - 0.75) < 0.001
    assert abs(processed[4] - 1.0) < 0.001
    
    # Check average (should be 0.5)
    average = interpreter.traditional.global_env['average']
    assert abs(average - 0.5) < 0.001


def test_knowledge_graph_with_logic():
    """Test knowledge graph representation using logic programming with direct API"""
    from bayan.logical_engine import LogicalEngine, Fact, Rule, Predicate, Term

    engine = LogicalEngine()

    # Add entity facts
    engine.add_fact(Fact(Predicate('entity', [Term('john'), Term('person')])))
    engine.add_fact(Fact(Predicate('entity', [Term('mary'), Term('person')])))
    engine.add_fact(Fact(Predicate('entity', [Term('acme_corp'), Term('company')])))
    engine.add_fact(Fact(Predicate('entity', [Term('python_lang'), Term('skill')])))

    # Add relationship facts
    engine.add_fact(Fact(Predicate('works_at', [Term('john'), Term('acme_corp')])))
    engine.add_fact(Fact(Predicate('works_at', [Term('mary'), Term('acme_corp')])))
    engine.add_fact(Fact(Predicate('has_skill', [Term('john'), Term('python_lang')])))
    engine.add_fact(Fact(Predicate('has_skill', [Term('mary'), Term('python_lang')])))

    # Add inference rule: colleague(X, Y) :- works_at(X, C), works_at(Y, C).
    head = Predicate('colleague', [Term('X', is_variable=True), Term('Y', is_variable=True)])
    body = [
        Predicate('works_at', [Term('X', is_variable=True), Term('C', is_variable=True)]),
        Predicate('works_at', [Term('Y', is_variable=True), Term('C', is_variable=True)])
    ]
    engine.add_rule(Rule(head, body))

    # Query: Who are colleagues?
    goal = Predicate('colleague', [Term('X', is_variable=True), Term('Y', is_variable=True)])
    result = engine.query(goal)

    # Should find that john and mary are colleagues
    assert len(result) >= 1

    # Check if we can find the colleague relationship
    colleagues = [(r.bindings['X'].value, r.bindings['Y'].value) for r in result]
    # Should have at least one colleague pair
    assert len(colleagues) >= 1
    # Should include (john, john), (john, mary), (mary, john), (mary, mary)
    assert ('john', 'mary') in colleagues or ('mary', 'john') in colleagues

