# rulesengine

Is there any developer liking to work with hundreds of chained if/else? If you're one of those this package isn't for you.

A rules engine is a way to structure your code as pipelines. The objective is to create chained modular and reusable rules with a simple structure structure :
* A `filter`: can I do some stuff?
* An `action`: I know I can do some stuff so I do it

With a rules engine you have to think your pipeline has stackable modules to generate easily readable pipelines.

## Example with some potatoes

Here is an example on how to (try to) eat smashed potatoes:
``` python3
# How to eat smashed potatoes
rules = RulesEngine()
rules.add(GetPotatoes)
rules.add(CookPotatoes)
rules.add(EatPotatoes)
rules.add(SmashPotatoes)
rules.add(EatSmashedPotatoes)
rules_output = rules.run()

rules_ouput.get("Eaten smashed potatoes portions")  # Sorry there is nothing
```

With a pipeline like this one, you won't eat any smashed potatoes but you'll
still have eaten some potatoes (if `GetPotatoes` got you at least one potato).
Let's see the `SmashPotatoes` rule to understand:

``` python3
class SmashPotatoes(Rule):
    RULE_NAME = "Smash potatoes"

    def filter(self, input_data):
        """
        Can I really smash potatoes?
        """
        # Get my smashable potatoes
        smashable_potatoes = input_data.get("cooked potatoes")
        # Have I any smashable potatoes ?
        if smashable_potatoes is None or smashable_potatoes < 1:
            # There isn't any potato to smash. We won't do any thing...
            return False
        # YES! We can smash potatoes!!!
        return True

    def action(self, input_data):
        """
        Let's smash potatoes because we can
        """
        # Get you potatoes
        smashable_potatoes = input_data.get("cooked potatoes")
        # Do your job (an other RulesEngine?)
        smashed_potatoes_portions = ...

        input_data.set("smashed potatoes portions", smashed_potatoes_portions)
        input_data.set("cooked potatoes", 0)
```

In this rule if the filter isn't applied, we won't apply the action :
* No `cooked potatoes` no action and finally no `smashed potatoes portions`
* At least 1 `cooked potatoes`, the action is performed and we have at least 1
`smashed potatoes portions`

## Installation

``` bash
pip install rulesengine
```

## Documentation & Help

### Create a rule

```python3
from rulesengine import Rule

class MyRule(Rule):
    RULE_NAME = "A minimal rule"

    # An execution order (positive or -1). Rules of same level are executed in their
    # declaration order. -1 are executed lastly and minimal values are executed firstly
    RULE_ORDER = -1

    def filter(self, input_data):
        """
        Test if you can apply your rule, are all variables initialized?
        """
        return True

    def action(self, input_data):
        """
        Do some stuff
        """
```

### Access data

An object is passed between rules and returned by the `RulesEngine.run()`
method : `RulesData`
```python3
# Get an element (return None if not initialized)
my_data.get('my element key')

# Set or update an element
my_data.set('my element key', something)

# Delete an element (let's free some memory!)
my_data.delete('my element key')

# Get previously executed rule
my_data.get_previous()

# Set expected next rule
my_data.set_expected_next(MyNextRule.RULE_NAME)
```

### Create pipeline

```python3
from rulesengine import RulesEngine

# Initialize the pipeline
rules = RulesEngine()
rules.add(MyRule, forced_order=0)  # Will be executed first
rules.add(MyRule)  # The same rule again
rules.add(AnOtherRule, previous_rule=MyNextRule.RULE_NAME)  # Won't match the previous rule condition
rules.add(AnOtherRule, converter=a_funtion) # Sometime, to reuse rules we need to do extra stuff before the rule
rules_output = rules.run()
```

Pipelines doesn't have to be run to the end

```python3
from rulesengine import RulesCourse

# Run every runnable rules (default)
rules = RulesEngine(rules_course=RulesCourse.non_blocking)

# Stop on the first rules's filter returning False
rules = RulesEngine(rules_course=RulesCourse.block_on_false)

# Stop on the first rules's filter returning True
rules = RulesEngine(rules_course=RulesCourse.block_on_true)

# Raise an error on the first rules's filter returning False
rules = RulesEngine(rules_course=RulesCourse.error_on_false)
```

### Populate the pipeline before execution

```python3
# At creation
rules = RulesEngine({
        "data_1": 1,
        "data_2": list(),
    })

# afterward
rules.set(key, value)
```

### Manage errors

There is only one rulesengine error : `rulesengine.RulesEngineException`

## Contributing

As an open source project, rulesengine welcomes contributions of all forms (especially culinary but please don't send any potato, the smashing potato workflow will fail).
