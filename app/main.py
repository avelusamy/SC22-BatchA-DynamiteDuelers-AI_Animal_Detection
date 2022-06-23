from flask import send_from_directory
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import render_template
from url_utils import get_base_url
import os
import torch

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
status = "Endangered"
port = 11111
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

model = torch.hub.load("ultralytics/yolov5", "custom", path = 'best.pt', force_reload=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route(f'{base_url}', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('index.html')


@app.route(f'{base_url}/uploads/<filename>')
def uploaded_file(filename):
    here = os.getcwd()
    image_path = os.path.join(here, app.config['UPLOAD_FOLDER'], filename)
    results = model(image_path, size=416)
    if len(results.pandas().xyxy) > 0:
        results.print()
        save_dir = os.path.join(here, app.config['UPLOAD_FOLDER'])
        results.save(save_dir=save_dir)
        def and_syntax(alist):
            if len(alist) == 1:
                alist = "".join(alist)
                return alist
            elif len(alist) == 2:
                alist = " and ".join(alist)
                return alist
            elif len(alist) > 2:
                alist[-1] = "and " + alist[-1]
                alist = ", ".join(alist)
                return alist
            else:
                return
        confidences = list(results.pandas().xyxy[0]['confidence'])
        # confidences: rounding and changing to percent, putting in function
        format_confidences = []
        for percent in confidences:
            format_confidences.append(str(round(percent*100)) + '%')
        format_confidences = and_syntax(format_confidences)

        labels = list(results.pandas().xyxy[0]['name'])
        # labels: sorting and capitalizing, putting into function
        labels = set(labels)
        labels = [emotion.capitalize() for emotion in labels]
        labels = and_syntax(labels)
        # description define
        descriptions = {}
        descriptions['Monkey'] = "This type of animal is Endangered. Monkeys are small, active primates notorious for their mischievous nature.  There are many species of monkeys,  found throughout Asia, Africa, and Central and South America, but they possess high intelligence, range from less than a foot to 2 feet tall, and live in social groups. Monkeys generally have a playful nature, yet can also viciously attack humans when feeling threatened. Their habitat is located in forests, where they live in groups, and are omnivorous."
        descriptions['Lizard'] = "This type of animal is not Endangered.  Lizards are reptiles, with thousands of species  ranging from all shapes, sizes, and colors, with the biggest lizard being the komodo dragon,  which can grow up to 10 feet in length and nearly 200 lbs.  They are found worldwide, in diverse habitats, from deserts to mountains,  as well as being kept as pets. Being reptiles, they are sluggish in cold weather and active in warmer weather. Most lizards are carnivorous, though even the komodo dragon does not generally attack humans."
        descriptions['Alligator'] = "This type of animal is not Endangered. Alligators are large, powerful, fearsome-looking animals.  There are only two species of alligators, the American Alligator and the Chinese Alligator, with the former weighing up to 500 lbs and reaching up to 15 feet in length, and the latter reaching only up to half that size .  Both live in freshwater areas,  with the American Alligator found in the southern United States, in freshwater swamps and rivers. However, although the American Alligator is of Least Concern, the Chinese Alligator is critically endangered."
        descriptions['Zebra'] = "This type of animal is Endangered. Zebras are known for their distinct striped pattern. They are fairly large animals, and between the four main species, the average weight is 815 pounds. They prefer living in the African savanna woodlands and grasslands without trees, but the availability of their habitat is declining. Zebras are herbivores, and almost only eat grasses. Many populations and subpopulations have been heavily depleted due to humans."
        descriptions['Pig'] = "This type of animal is not Endangered. Pigs have 8 different species, which include domestic and wild pigs. More commonly known is the domestic pink pig. The average size of a domestic pig is 300 to 700 pounds and has a typical lifespan of 6-10 years on a farm or up to 15-20 years if kept as a pet. A few of the different ecosystems that you can find wild pigs in include rainforests, scrubby secondary forests, mangroves, swamps, grasslands, and more. Whereas domestic pigs mainly live in pastures and farmland. They are omnivorous, and mainly eat food found underground, such as grubs."
        descriptions['Sheep'] = "This type of animal is not Endangered. Sheep have 5 different species, but they share distinct characteristics.  They are about 3 ft. tall on average, and larger individuals can weigh up to 350 pounds or more. Most sheep are domesticated, therefore the habitat they live in is up to their owners which is usually pastures or farmland. Undomesticated sheep usually live in mountains and hilly regions. Sheeps are herbivorous and primarily feed on grasses. These domestic mammals would not exist without human interaction."
        descriptions['Tiger'] = "This type of animal is Endangered. Tigers have 9 subspecies and are known for their distinct black and orange striped pattern. These cats can stand as tall as 4 feet, and weigh over 800 pounds in the wild. The optimal habitat for tigers is located close to a water source, has lots of vegetation for cover while hunting, and plenty of prey. Different subspecies can be found in a number of forest types, including evergreen, swamp, mangrove, deciduous, thorn, and taiga. They will also occasionally inhabit rocky mountain habitats, as well as savannas and grasslands. Tigers are carnivores and primarily hunt animals 200 pounds or more. Humans have been consistently decimating tiger populations for years."
        descriptions['Cow'] = "This type of animal is not Endangered. A Cow is an active and large animal, the average male weighs 2,400 pounds, and the average female weighs 1,600 pounds. Cattle utilize many habitats, such as savannas, scrub forests, and even desert edges. As long as they have lots of space and plenty of grass, Cattle are happy. They are herbivores, and mainly eat plants. Humans rely on Cattle for many purposes and interact frequently with each other since they are domesticated animals."
        descriptions['Bird'] = "This type of animal is not Endangered. There are more than 10,400 species of birds and they all have their own unique feathers and colors. There are five basic sizes of birds, from very small (3 to 5 inches) to very large (32 to 72 inches). Birds habitat needs to a place where they have shelter or cover to serve as protection from the weather and a safe place to raise a family. Birds are found worldwide. Most birds are omnivores, and mainly eat plants, nuts, and small mammals. Some humans keep birds as pets."
        descriptions['Horse'] = "This type of animal is “ + status + “. Horses are large mammals that vary in color and size. The shortest horse is 3 feet weighing 200 pounds, whereas the tallest is 6 feet weighing 2,400 pounds. They have been domesticated by humans, and therefore mainly live in pastures and fields and are present worldwide. In some cases, horses are bred to be racers. As herbivores, these creatures feed exclusively on plants, mainly grasses."
        descriptions['Dog'] = "This type of animal is not Endangered. Dogs are energetic and loving animals. They have many breeds, which includes dogs of various colors, sizes, and personalities. The lightest dog breed weighs a single pound, whereas the heaviest weighs around 200 pounds. Dogs are domesticated animals that mainly live with their owners, and dogs are present worldwide. They are omnivores, and have a strong connection with humans."
        descriptions['Panda'] = "This type of animal is Endangered.  The giant panda (or just panda bear) is a large, powerful animal that is also well-known for being quite lazy and sluggish. The average weight for a male panda bear is 220-250 pounds, with females weighing a little less than that range. Their habitat is located in the mountainous areas of China, where their diet consists solely of bamboo."
        descriptions['Bear'] = "This type of animal is not Endangered.  Bears are the largest land mammals, with some species, such as the polar bear and grizzly bear, can weigh over a ton, and are far larger than the average human.  Bears’ habitats are found in the Americas, Eurasia, and the Arctic. While not normally aggressive to humans, they might attack out of desperation or feeling threatened.  Depending on the species, bears are herbivorous, omnivorous, or carnivorous. "
        descriptions['Cats'] = "This type of animal is not Endangered. Cats are small, agile animals,  who are sociable and affectionate to their owners on their own terms. A popular pet, cats have been domesticated for thousands of years, with many different breeds with different colors and sizes, with most ranging around a little above or below a foot tall. Cats are often independent, being able to catch their own food, and enjoy roaming on their own."
        descriptions['Elephant'] = "This type of animal is Endangered. There are 2 main species of elephants, the African and Asian, both of whom share very similar characteristics. The largest land animals on Earth, elephants stand at 10-13 feet tall, and weigh 7,500kg. Elephants migrate through many landscapes, such as forests and savannas. They are scarce in the wild, and travel in groups. Elephants are herbivores, eating up to 100kg from a range of leaves, grasses, fruits, and roots. Elephants are wild animals and live away from human settlements, though in many parts of Asia and Africa elephants can be found in zoos or available to ride."
        return render_template('results.html', confidences=format_confidences, labels=labels, descriptions = descriptions[labels], old_filename=filename, filename=filename)
    else:
        found = False
        return render_template('results.html', labels='No Supported Animals', old_filename=filename, filename=filename)


@app.route(f'{base_url}/uploads/<path:filename>')
def files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'https://cocalc13.ai-camp.dev'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
