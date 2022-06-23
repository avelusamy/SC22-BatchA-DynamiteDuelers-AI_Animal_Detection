# AI Animal Detection
An AI project made by AI Camp students.

### Product Spec
#### Overview:
 We are going to make a system that takes an image of an animal, identifies the animal, and determines whether it is endangered or not.
#### Our Goals:
Sections to train AI: Endangered (E) and Non-Endangered (NE) animals
Identifying the animal name (these are the animals we can identify):
Dogs, Birds, Cats, Pandas, Polar Bear, Lizards, Tiger, Zebras, Monkeys, Horses, Pigs, Cows, Sheep, Elephants, and Crocodiles/Alligators

Let people know the status of endangerment in 1 way:
Add a little description (ex. We think this is an endangered Panda with 99% confidence.)

#### Why we are making this:
	
 As a group, we have a strong liking for animals. Therefore, we wanted to integrate that into our product. It is important to spread awareness of endangered animals, so we decided to include it as part of our product also. Additionally, having this component makes it a better product in terms of usefulness. This kind of software can use drones to determine whether there are endangered animals. Another example of applying this software to help people is during their hikes or outdoor activity. If they see an animal and wonder if it is endangered or not, they can use our software.

#### Basic Outline: 

First, we will add multiple images of the animals that we have included above and labels them. This will act as our data set, which we will use to train the AI to recognize the animals. Once this data set is finalized, we will start using these images for the AI to look for. When the AI is trained well, we will begin teaching it to identify endangerment status. After the AI has been trained well in endangerment statuses, we will start working on the website and website design. 
The end result is an AI system that will determine the type of animal in an image as well as its endangerment level. It will let the user know the animal type and a description of the animal’s status, along with how confident it is. Additionally, it will also identify whether the animal is endangered or not endangered. It will then display this to the user in the description. 

#### What an MVP Looks Like:

Our MVP at least identifies the type of animal. This is the most important step in completing our goal. This is because to identify the endangerment status of an animal we need to establish which animal it is. Once the animal is identified, the MVP includes telling the user what type of animal it is.

#### Type of ML problem:
	
 This product is trying to use Python and YOLO to recognize animals using computer vision AI software. The type of computer vision we are using is object detection; the user provides an image and with the program, we detect the animal in the image. This animal is the so-called “object” we are trying to detect.
Tech Stack:
#### We used:
##### YOLO

To train the model to recognize specific animals

To get the AI software that includes confidence

##### Google

To find images to train the model to recognize certain animals

To find the endangerment status of the animals

To find python snippets to assist during the coding process

##### Cocalc

To write the program and execute the python code

To train the model

#### Roadblocks:

##### Confusing animals with other animals

Adding more data/images for the computer to train with so it becomes more familiar with the animal

##### Image distortion

Let the user know the image is distorted/not high enough quality

The user inputs an image with animals that weren’t included

Teach it to say “Animal Not Supported” and add a message stating which animals the computer can identify.

##### Styling The Website

Using the web and our instructor as a resource to solve the problems
