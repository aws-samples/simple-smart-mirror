# Smart Mirror Challenges

__Challenges:__
<!-- AUTO-GENERATED-CONTENT:START (TOC) -->
- [Change smart-mirror invocation name](#change-smart-mirror-invocation-name)
- [Change Mirror Wakeword Activation color](#change-mirror-wakeword-activation-color)
- [Show Color on all LEDs with Alexa](#show-color-on-all-leds-with-alexa)
- [Deploy Clock functionality](#deploy-clock-functionality)
- [Make Clock Respond to Invocation word "show clock"](#make-clock-respond-to-invocation-word-show-clock)
- [Update and add clock invocation intents/samples](#update-and-add-clock-invocation-intentssamples)
- [Visualize Timer with LEDs](#visualize-timer-with-leds)
<!-- AUTO-GENERATED-CONTENT:END -->

> NOTE! If you ever get stuck when doing challenges you can compare with what is available in `smart-mirror-full/extracted` folder in this repository

## Change smart-mirror invocation name

On example code Smart Mirror activation word is "Unicorn"

> User: Alexa, open *Unicorn*

or

> User: Alexa, *Unicorn*

The challenge is to update this to something else you like.

Please see additional information how the simple smart mirror works in this [documentation](docs/HOW_IT_WORKS.md)

Additional details on how to work with Git: https://docs.gitlab.com/ee/gitlab-basics/
And further details on Cloud9 IDE https://docs.aws.amazon.com/cloud9/latest/user-guide/source-control-gitpanel.html

> Tip: As everything is CI/CD driven you should do change in repository (interactionModels/custom/en-US.json)

Configuring Invocation name for custom skill:
https://developer.amazon.com/en-US/docs/alexa/custom-skills/choose-the-invocation-name-for-a-custom-skill.html


<details>
  <summary>See Answer how to change smart-mirror invocation name</summary>

1. Open Cloud9 IDE and browse to your smart-mirror source code
2. Update value for "invocationName" in interactionModels/custom/en-US.json
3. Add, commit and push your code
```
git add .
git commit -m "Updated invocation word"
git push
```
4. After a while (see code pipeline) your device get's new code (and this is also pushed to Amazon Developer Console  / Alexa Custom Skill)
5. Validate the change by activating skill with new invocation word (Note! it takes few minutes for skill to update)

</details>

---

## Change Mirror Wakeword Activation color

On our example mirror "activation color" is yellow (What mirror reacts when you use your Alexa activation word).

The challenge is to update this to something else you like.

Please see additional information how the simple smart mirror works in this [documentation](docs/HOW_IT_WORKS.md)

Additional details on how to work with Git: https://docs.gitlab.com/ee/gitlab-basics/
And further details on Cloud9 IDE https://docs.aws.amazon.com/cloud9/latest/user-guide/source-control-gitpanel.html

> Tip:  This is worked in `script/agt_smart_mirror.py`

<details>
  <summary>See Answer How to update Activation Color</summary>

1. Open Cloud9 IDE and browse to your smart-mirror source code
2. Update value for webcolors.name_to_rgb('`yellow`') in script/agt_smart_mirror.py to something you like better (example `red`)

```python
        #default options for show color as a reference
        self.showColorOptions = {
            'color': webcolors.name_to_rgb('yellow') # Change this to color of your choosing
        }
```

3. Add, commit and push your code
```
git add .
git commit -m "Changed activation color"
git push
```
4. After a while (see code pipeline) your device get's new code (and this is also pushed to Amazon Developer Console  / Alexa Custom Skill)
5. Validate the change by using your Alexa activation word and seeing new color

</details>

---

## Show Color on all LEDs with Alexa

In the previous challenge you learned how to change the color when your Alexa is activated with the wakeword ("Alexa", "Echo"). 

In this challenge we want to explore how we can light up all LEDs with a color of our choosing with the help of Alexa. We want you to
say something like "Change color to blue". So after activating the smart mirror skill with "Alexa, open unicorn" (or your invocation word) - say "Change color to blue". The LEDs should then turn blue.

Please see additional information how the simple smart mirror works in this [documentation](docs/HOW_IT_WORKS.md)

There are 3 main problems to solve for this challenge. 1/ How can I tell Alexa what color I want and 2/ how can the Alexa device tell our gadget (the Raspberry Pi) that it should do something and 3/ How will I change the user input "Purple" into something the LEDs strip understands.

For 1/ check out the list of available built-in slot types [here](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#list-slot-types). If you want to know more about the basic building blocks of an Alexa Skill please read [Create Intents, Utterances, and Slots](https://developer.amazon.com/en-US/docs/alexa/custom-skills/create-intents-utterances-and-slots.html).

For 2/ have a look at the following [documentation](https://developer.amazon.com/en-US/docs/alexa/alexa-gadgets-toolkit/understand-alexa-gadgets-toolkit.html) to understand how the Alexa device and the gadget communicate.


![](https://images-na.ssl-images-amazon.com/images/G/01/mobile-apps/dex/gadgets-toolkit/agt-overview-with-skill._TTH_.png)


For 3/ please have a look at the following open source library: https://github.com/ubernostrum/webcolors The pip module was already installed during the setup process you followed earlier and is ready for use. Please have a closer look at the documentation [Changing from color names to other formats](https://webcolors.readthedocs.io/en/1.11.1/contents.html#conversions-from-color-names-to-other-formats). The library that is used to change the colors of the LEDs uses the RGB format to describe colors. Find out more about RGB [here](https://en.wikipedia.org/wiki/RGB_color_model)

To add this functionality you will have to modify the following files:

* interactionModels/custom/en-US.json
* lambda/custom/lambda_function.py
* device/script/agt_smart_mirror.py

> Hint: Look at how "ShowRainbow" is implemented. You will very useful code in the above files that you can use to solve this challenge.

<details>
  <summary>See how to change the color via Alexa</summary>

1. Open Cloud9 IDE and browse to your smart-mirror source code
2. Open interactionModels/custom/en-US.json and add the following intent to the intents (for example after the "ShowRainbow" intent)

```json
      {
          "name": "ShowColor",
          "slots": [
              {
                  "name": "Color",
                  "type": "AMAZON.Color"
              }
          ],
          "samples": [
              "Show color {Color}",
              "{Color} color",
              "Change color to {Color}",
              "Turn color to {Color}"
          ]
      }
```
Feel free to add or remove sample utterances. AMAZON.Color supports a wide range of colors and works well for this example. The alternative is to build a custom slot type [Custom Slot Types](https://developer.amazon.com/en-US/docs/alexa/custom-skills/create-and-edit-custom-slot-types.htm). 

We define how our Alexa Skill can interact with the user in this file. You will find other intents in the file that might be interesting to explore. Notice that we use a mix of built-in Intents like AMAZON.StopIntent and custom intents like ShowRainbow.

3. Open lambda/custom/lambda_function.py and add two new function to handle the "Show Color" intent

```python
      @skill_builder.request_handler(can_handle_func=is_intent_name("ShowColor"))
      def yes_intent_handler(handler_input: HandlerInput):
          logger.info("ShowColor received. Sending color to device.")
          color_slot = "Color"
          
          # Retrieve the stored gadget endpointId from the SessionAttributes.
          session_attr = handler_input.attributes_manager.session_attributes
          endpoint_id = session_attr['endpointId']

          response_builder = handler_input.response_builder
          
          slots = handler_input.request_envelope.request.intent.slots

          if color_slot in slots:
              color = slots[color_slot].value
              (response_builder
              .speak(f'Alright. Lighting up in {color}')
              .add_directive(build_showcolor_directive(endpoint_id, color))
              .set_should_end_session(True))
          else:
              (response_builder
              .speak("Can you please repeat that?")
              .set_should_end_session(False))


          return response_builder.response

      def build_showcolor_directive(endpoint_id, color):
          return SendDirectiveDirective(
              header=Header(namespace='Custom.SmartMirror', name='Color'),
              endpoint=Endpoint(endpoint_id=endpoint_id),
              payload={
                  'color': color
              }
          )

```

This lambda is the backend of our Alexa skill. Here we can react to user input, fetch results, ask for clarifications and send instructions to our Alexa device. The *@skill_builder.request_handler* of the added function will handle requests to the ShowColor intent. If Alexa was able to pick up a color we will have the the user input available in requests slots. In this case we will prompt the user to repeat the request if we did not catch a color. 

Another interesting aspect of this piece of code is when we send text to the Alexa device via the speak function. We also send a directive to the assistant. The directive is a message that will be passed on to our gadget (the Raspberry Pi). The directive message is created in the *build_showcolor_directive* function. It contains a namespace, a name and a payload with the color. This will be important in the next step.

4. Open /device/script/agt_smart_mirror.py and add the following function to the SmartMirrorGadget Class

```python
        # this matches the namespace that the skill adds in the payload (see lambda_function.py): (namespace='Custom.SmartMirror', name='Color'),
        def on_custom_smartmirror_color(self, directive):
            """
            Handles Custom.SmartMirror.Color directive
            """
            payload = json.loads(directive.payload.decode("utf-8"))
            color = payload['color'].lower() #this is the color name coming in from Alexa
            rgb = webcolors.name_to_rgb(color)
            logger.info(f'show color directive called with color {color} => {rgb}')

            self.showColorOptions['color'] = rgb        
            self.startAction(Actions.ShowColor)
```

When the Alexa device receives the ShowColor directive from the Skill it knows to forward it to the Gadget. This is because we have configured the Alexa device to notify the Gadget by adding the namespace "Custom.SmartMirror" in device/script/smart_mirror_service_start.ini (This has happened as part of the initial setup). All we have to do now is to follow a convention for the function that is supposed to receive the directive: on_{namespace}_{name}. The function name needs to be lower case and replace the "." with an underscore. 
The directive contains the color the user selected in the payload. The last thing to do now is to convert the color name to an RGB value and start the ShowColor action on the LEDs. 
Check out the *loop* function in /device/script/agt_smart_mirror.py to see what happens when you call *self.startAction(Actions.ShowColor)*. The actual function that changes the color on the LED strip can be found in /device/script/smart_mirror.py -> *showColor*

5. Add, commit and push your code
```
git add .
git commit -m "Changed activation color"
git push
```
6. After a while (see code pipeline) your device get's new code (and this is also pushed to Amazon Developer Console  / Alexa Custom Skill). You will only be able to test your changes after the entire pipeline is complete.
7. Validate the change by saying "Alexa, open unicorn" (or your invocation word) - then say "Change color to blue". The LEDs should then turn blue.

</details>

---

## Deploy Clock functionality

Having a 60 LED strip on round object like mirror is cool - but what is even cooler is how to use this to show current time - and eventually control it through voice. Let's now build on what we have learned on previous challenge.

The first challenge is to build logic that shows a 12 hour clock in your smart mirror as default action.

In this challenge we build a clock logic that shows time with LED's lit as follows:
- green is second
- blue is minute
- red is hour

Please see additional information how the simple smart mirror works in this [documentation](docs/HOW_IT_WORKS.md)

For clock activity you need to modify following files:

* script/agt_smart_mirror.py
  - Alexa Gadget Skill skill
* script/smart_mirror.py
  - Clock Logic

<details>
  <summary>See Answer how to create a clock functionality</summary>

1. Open Cloud9 IDE and browse to your smart-mirror source code

2. Update script/agt_smart_mirror.py
<details>
  <summary>Add class Action</summary>

Add Clock = next free number, in below example this is 4

```python
class Actions(Enum):
    Off = 0
    Rainbow = 1
    Breathe = 2
    ShowColor = 3
    Clock = 4    # This is added for Clock
```
  </details>

<details>
  <summary>Update self.defaultAction to be Clock</summary>

```python
    """
    An Alexa Gadget for your simple smart mirror.
    """
    def __init__(self):
        super().__init__()

        self.config = self.get_parameters()
        self.smart_mirror = SmartMirror(self.config)

        #This sets what action is started when the mirror starts
        self.defaultAction = Actions.Clock # This is updated to show Clock
```
  </details>

<details>
  <summary>Loop self action handling</summary>

under def loop(self) - handle Actions.Clock:
```python
                    if self.currentAction == Actions.Clock:
                        self.smart_mirror.clock()
```

Add payload handling:

```python
    # this matches the namespace that the skill adds in the payload (see lambda_function.py): (namespace='Custom.SmartMirror', name='Clock'),
    def on_custom_smartmirror_clock(self, directive):
        """
        Handles Custom.SmartMirror.Clock directive
        """

        logger.info('show clock directive called')

        self.startAction(Actions.Clock)
```
  </details>

3. update script/smart_mirror.py

<details>
  <summary>Add main clock logic</summary>

```python
    def clock (self):
        print("Showing Clock")
        self.reset()
        num_pixels = self.config.LedCount
        now = datetime.now()
        hourval = (now.hour % num_pixels % 12) # Adapt to led count, and set 12 hour clock (0-11)
        minutepixel = (now.minute  // (60 // num_pixels) % num_pixels) # Adapt to non 60 led count if needed
        secondpixel = (now.second // (60 // num_pixels) % num_pixels) # Adapt to non 60 led count if needed
        hourpixel = (hourval * 60 + minutepixel) // 12 # Adjusted position relative to minutes   

        ## Define used colors - see how to pass this
        hourcolor = (255,0,0)
        minutecolor = (0,0,255)
        secondcolor = (0,255,0)
        ## Turn on hour - minute - second pixels using ShowPixel function
        self.showPixel(hourpixel,hourcolor)
        self.showPixel(minutepixel,minutecolor)
        self.showPixel(secondpixel,secondcolor)
```
  </details>

4. Add, commit and push your code
```
git add .
git commit -m "Added clock functionality as default action"
git push
```
5. After a while (see code pipeline) your device get's new code (and this is also pushed to Amazon Developer Console  / Alexa Custom Skill)
6. Validate the change - you should see clock in your smart mirror as default action

</details>

---

## Make Clock Respond to Invocation word "show clock"

Previously we build clock functionality and added that as default action for smart mirror.

What if we want this to be available through Alexa ?

Challenge is to add to your clock a logic that opens when you say "show clock" in your smart mirror skill.

And make this activate with `invocation` / sample "show clock"

Please see additional information how the simple smart mirror works in this [documentation](docs/HOW_IT_WORKS.md)

To add invocation word to your clock you need to modify following files:

* interactionModels/custom/en-US.json
* lambda/custom/lambda_function.py

<details>
  <summary>See Answer</summary>

1. Open Cloud9 IDE and browse to your smart-mirror source code
2. Update interactionModels/custom/en-US.json
<details>
  <summary>Update Intent for Clock ShowClock</summary>

```python
                {
                    "name": "ShowClock",
                    "slots": [],
                    "samples": [
                        "show clock"
                    ]
                }
```

  </details>

3. Update lambda/custom/lambda_function.py

<details>
  <summary>Handle intent and build clock directive</summary>

Add Clock to help intent handler:

```python
@skill_builder.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input: HandlerInput):
    logger.info("Received HelpIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("You can say rainbow or show clock") # Updated "show clock" when help is called
            .set_should_end_session(False)
            .response)
```

Clock intent handler:

```python
@skill_builder.request_handler(can_handle_func=is_intent_name("ShowClock"))
def clock_intent_handler(handler_input: HandlerInput):
    logger.info("Received *** ShowClockIntent ***")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("Super! Showing clock")
            .add_directive(build_clock_directive(endpoint_id))
            .set_should_end_session(True)
            .response)
```

Build Clock Directive:

```python
def build_clock_directive(endpoint_id):
    return SendDirectiveDirective(
        header=Header(namespace='Custom.SmartMirror', name='Clock'),
        endpoint=Endpoint(endpoint_id=endpoint_id),
        payload={}
    )
```

  </details>


3. Add, commit and push your code
```
git add .
git commit -m "Updated Clock Invocation functionality"
git push
```
4. After a while (see code pipeline) your device get's new code (and this is also pushed to Amazon Developer Console  / Alexa Custom Skill)
5. Validate the change - Activate your smart mirror skill in Alexa *your Invocation word* and "show clock". You can also say "help" to get help.

</details>

---

## Update and add clock invocation intents/samples

Calling your clock with <invocation> "Show Clock"is nice - but we can do better!

 Challenge is to update intents for clock to include:
- "What is the time"
- "Clock"
- "Time"
- "Show 3 led's"

Tip:
https://developer.amazon.com/en-US/docs/alexa/alexa-gadgets-toolkit/receive-custom-event-from-gadget.html

<details>
  <summary>Update Invocation Samples</summary>

1. Open Cloud9 IDE and browse to your smart-mirror source code
2. Update File Update interactionModels/custom/en-US.json "ShowClock" intent

```python
                {
                    "name": "ShowClock",
                    "slots": [],
                    "samples": [
                        "show clock",
                        "What is the time?",
                        "Clock",
                        "Time",
                        "Show 3 led's"
                    ]
                }
```

3. Add, commit and push your code

```
git add .
git commit -m "Updated Clock Invocation samples"
git push
```
4. After a while (see code pipeline) your device get's new code (and this is also pushed to Amazon Developer Console  / Alexa Custom Skill)
5. Test your new samples with Alexa
</details>

---

## Visualize Timer with LEDs

This challenge will help us to visualize a standard timer that is running on you Alexa device. When you start a timer by saying "Alexa start 10 minute timer" the LEDs will be used to show how far the timer has come. No LEDs will be turned on at the very beginning. 30 LEDs will be turned on after 5 minutes and all will be lit when the timer elapses after 10 minutes.

In this challenge we will make use of of a built-in directive that gets triggered as a reaction to native Alexa capability. This works just like the already implemented wakeword activation. You can find out which build-in directives can be sent to your device [here](https://developer.amazon.com/en-US/docs/alexa/alexa-gadgets-toolkit/understand-alexa-gadgets-toolkit.html).

As a prerequisite we must ensure that our gadget gets informed about this event by Alexa. This has already been done as part of the setup, but please check out the file device/script/smart_mirror_service_start.ini anyways. The important bit is the following:

```
  Alerts = 1.1
```

This makes sure we can react to alert changes which includes timers.

The problems to solve in this challenge is to 1/ hook up to the timer activated and deleted event 2/ Extract all relevant timer information from the directive sent by the Alexa device and 3/ Calculate how many LEDs should be turned on for each iteration through the *loop* function in *device/script/agt_smart_mirror.py* 

For 1/ and 2/ check out the interface documentation [here](https://developer.amazon.com/en-US/docs/alexa/alexa-gadgets-toolkit/alerts-interface.html)

For 3/ use your creativity or use the hidden hints below.

To add this functionality you will have to modify the following file:

* device/script/agt_smart_mirror.py

<details>
  <summary>Hints</summary>

1. Open Cloud9 IDE and browse to your smart-mirror source code
2. Open and modify device/script/agt_smart_mirror.py

3. Locate the Actions enumeration and add a new action for the Timer

```python
      class Actions(Enum):
          Off = 0
          Rainbow = 1
          Breathe = 2
          ShowColor = 3
          Clock = 4
          Timer = 5
```

We need to add this action so the *loop* function is aware of the new Action. We will jump into the loop function later to implement the necessary changes.

4. Now scroll down a bit to the constructor of SmartMirrorGadget class. Add the default options below the showColorOptions

```python
    #default options for timer
    self.showTimerOptions = {
        'startTime': None,
        'endTime': None,
        'color': webcolors.name_to_rgb('red'),
        'timer_token': None
     }
```

Here we initialize the timer options we will be using later. You can ignore most of the settings for now, but you might want to change the color of the LEDs.

5. Now let's add the Timer action to the *loop* function. You can add the following code snippet after the ShowColor block:

```python
    if self.currentAction == Actions.Timer:
        timerPosition = self.getCurrentTimerPosition()
        if(timerPosition != 0):
            self.smart_mirror.showRange(0, timerPosition, 0.1, self.showTimerOptions['color'])
        else:
            self.smart_mirror.showColor(self.showTimerOptions['color'])
```

Now the loop is aware of the Timer action and if the action is active it will call the *getCurrentTimerPosition* function. We will implement this function shortly. If the *getCurrentTimerPosition* function returned a valid value we use the existing function *showRange* of device/script/smart_mirror.py. The function lights up LEDs from index 0 to the variable timerPosition. If your LED strip has 60 LEDs and the timer is set for 10 minutes you should get a timerPosition=30 when there 5 minutes left on the timer. Also notice that we are using the color of the previous defined *showTimerOptions* variable.

6. Before we implement the *getCurrentTimerPosition* let us look at how we can be notified when a new timer has been set. For this add the following two functions to the SmartMirror Gadget:

```python
    def on_alerts_setalert(self, directive):
        """
        Handles setting of alerts on your connected Alexa device e.g. "Alexa set timer for 60 seconds"
        """
        if directive.payload.type != 'TIMER':
            logger.info(
                "Received SetAlert directive but type != TIMER. Ignorning")
            return

        endTime = dateutil.parser.parse(directive.payload.scheduledTime).timestamp()
        now = time.time()

        if endTime <= 0:
            logger.info(
                "Received SetAlert directive but scheduledTime has already passed. Ignoring")
            return

        if self.showTimerOptions['timer_token'] == directive.payload.token:
            logger.info(
                "Received SetAlert directive to update to currently running timer. Adjusting")
            self.showTimerOptions['endTime'] = endTime
            return

        if self.currentAction == Actions.Timer:
            logger.info(
                "Received SetAlert directive but another timer is already running. Ignoring")
            return

        logger.info("Received SetAlert directive. Starting a timer. " +
                    str(int(endTime - now)) + " seconds left..")
        self.showTimerOptions['endTime'] = endTime
        self.showTimerOptions['startTime'] = now
        self.showTimerOptions['timer_token'] = directive.payload.token
        self.showTimerOptions['color'] = webcolors.name_to_rgb('red')

        self.startAction(Actions.Timer)

    def on_alerts_deletealert(self, directive):
        """
        Handles deletion of alert - reverts back to default action
        """
        self.startAction(self.defaultAction)
```

To hook up to the events sent by the Alexa device we have to implement on_alerts_setalert and on_alerts_deletealert. You can read up about the interface [here](https://developer.amazon.com/en-US/docs/alexa/alexa-gadgets-toolkit/alerts-interface.html). The delete method is easy, when a timer is cancelled or elapsed we want to show the default action that we specified in the options (Clock, Rainbow or whatever you have configured).
The setalert function is mainly used to parse the directive. We need to find out when the timer was started and when it will finish. We need to store this data somewhere so we can calculate the timer position in *getCurrentTimerPosition*. We are using the timer options for that. The code also contains a couple of safegurads. It checks for example if there is already another timer running, if so the old one is replaced as we can only visualize one timer at a time with the current implementation.  

> Extra Challenge: Can you think of a way that makes it possibilities to visualize 2 timers at the same time?


7. Now we only have one thing left to to before we can commit and deploy our code and that is to implement the *getCurrentTimerPosition*. Add a new function to the SmartMirrorGadget Class:

```python
    def getCurrentTimerPosition(self):
        """
        Figure out how many LEDs should be turned on. If the timer is up all 60 LEDs shoul be lit.
        """
        start_time = self.showTimerOptions['startTime']
        end_time = self.showTimerOptions['endTime']
        current_time = time.time()
        timer_total = int(end_time - start_time)

        timer_left = int(max(0, end_time - current_time))

        if timer_left > 0:
            nextPosition = int((timer_total - timer_left)/timer_total * self.config.LedCount)
            time.sleep(1)
            return nextPosition  # Light up the leds
        else:
            return 0
```

The functions purpose is to read the current timers options to find out 1/ when has the timer started 2/ when does it end and 3/ how much time is left. With that data we have to figure out the number of LEDs to light up. We can use the variable *self.config.LedCount* to find out how many LEDs we have.



8. Add, commit and push your code

```
git add .
git commit -m "Updated Clock Invocation samples"
git push
```
9. After a short while (see code pipeline) your device get's the updated code. You do not need to wait until the skill is redeployed as we have not made any changes to the skill.
10. You can validate your changes by saying "Alexa set timer for 60 seconds". Your LEDs should now slowly fill up until all of them are turned on with the configured color. 
</details>

---
