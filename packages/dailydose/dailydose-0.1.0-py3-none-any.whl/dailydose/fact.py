import os
import json
import random

fun_facts = [
    {
        "heading": "Banging your head against a wall for one hour burns 150 calories.",
        "content": "If you're not keen on losing brain cells, you might want to give this calorie-burning idea a miss.\nA safer way to burn 150 calories would be to take your dog for a walk for 45 minutes.\nYou can also check out these other weird facts on ways to burn calories."
    },
    {
        "heading": "In Switzerland, it is illegal to own just one guinea pig.",
        "content": "While this may sound like an odd law to try and enforce, it actually makes perfect sense!\nGuinea pigs are social animals. They would become lonely or depressed, which is a form of animal cruelty these days.\nThe real question you should be asking is why this isn't a law everywhere?!"
    },
    {
        "heading": "Pteronophobia is the fear of being tickled by feathers.",
        "content": "If you've ever felt uneasy around feather blankets or pillows, this could be why!\nPteronophobia is the fear of feathers tickling you. In extreme cases, it can involve the fear of feathers in general.\nPteronophobia is made up of the Greek word ptero, meaning “feather,” and phobia, meaning “fear.”"
    },
    {
        "heading": "Snakes can predict earthquakes.",
        "content": "Many animals are able to predict earthquakes to varying levels of success. Yet, snakes are the most reliable, sensing earthquakes from as far as 75 miles away (121 km).\nWhat's more impressive is that they can sense an earthquake as many as five days before it actually occurs!\nWhen snakes sense an earthquake, they often leave their nests, even if the temperature is too cold.\nWhy not check out these other interesting facts about snakes."
    },
    {
        "heading": "Crows often hold grudges against specific people.",
        "content": "Crows are excellent at recognizing people's faces and are able to remember people for a long time!\nThis can be either a negative or positive fact, depending on how nice you are to them.\nWhile crows can tell us apart, we would find it difficult to distinguish one crow from another."
    },
    {
        "heading": "The oldest “your mom” joke was discovered on a 3,500-year-old Babylonian tablet.",
        "content": "In 1976, archaeologists discovered a tablet in Iraq, which has since been lost. But, researchers were able to analyze and translate the text from a photograph of the tablet.\nThe results? We know that the tablet does indeed contain jokes, but the full meaning has been lost in translation.\nThe translated form of the world's oldest your mom joke is “…of your mother is by the one who has intercourse with her. What/who is it?”\nDo we understand it? Not a chance, but we recognize a “your mom” joke when we see one!"
    },
    {
        "heading": "Two infectious diseases have been successfully wiped out: Smallpox and Rinderpest.",
        "content": "Due to advances in medical science, we successfully eradicated smallpox. The last natural case occurred on October 25, 1975.\nSmallpox causes breakouts of pus-filled blisters all over your body. In most cases, this was life-threatening, so the eradication was a monumental achievement.\nThe second disease humans eradicated was Rinderpest. This disease was often found in cattle and is similar to measles. The last known case of Rinderpest was in 2001."
    },
    {
        "heading": "May 29 is officially “Put a Pillow on Your Fridge Day.”",
        "content": "The roots of this odd-sounding holiday go back hundreds of years, starting in the early 1900s.\nPeople in the 1900s didn't have refrigerators and instead would hang a piece of cloth in their larders.\nIt's believed that doing so brought luck, peace, and prosperity to the household.\nThe tradition adapted over time to fit the modern kitchen. Nowadays, families worldwide place a pillow on top of their fridge every year on May 29th.\nRead more about Put a Pillow on Your Fridge Day right here!"
    },
    {
        "heading": "Cherophobia is the irrational fear of fun or happiness.",
        "content": "Do you hate all things fun? You might have Cherophobia! People with this phobia tend to avoid any kind of situation that others might classify as fun or joyful.\nThe word Cherophobia is made up of the Greek words chero, meaning “to rejoice,” and phobia, meaning “fear.”\nFor any readers out there with Cherophobia, please stop reading these fun facts now!\nWe can't imagine the psychological pain you've gone through by reading this far already."
    },
    {
        "heading": "7% of American adults believe that chocolate milk comes from brown cows.",
        "content": "I know that seven percent doesn't sound like a lot, but it actually works out at 16.4 million American adults. So it's an alarming fact when you think about it.\nThis shows that one in ten Americans has a flawed understanding of basic science or where their food comes from.\nNext, they'll claim that bacon grows on trees!"
    },
    {
        "heading": "If you lift a kangaroo's tail off the ground, it can't hop.",
        "content": "Kangaroos use their tails for balance whilst hopping. So if you elevate their tail, they would have no balance and fall over.\nThere are cases where kangaroos have lost their tails and can still move around. But, it took them a long time to adjust, and they can only move small distances at a time!\nTheir tails aren't only for balance – they also act as a third leg, propelling them forward just as much as their legs do!\nDon't miss these other fun facts about kangaroos."
    },
    {
        "heading": "Bananas are curved because they grow towards the sun.",
        "content": "Philosophers have pondered the shape of bananas for a long time, arguing until the sun goes down as to why they're curved.\nBananas go through a process called “negative geo-tropism.” This process causes the fruit to grow upwards towards the sun instead of towards the ground.\nThis, in turn, gives the banana its familiar curved shape.\nLove bananas? You'll go bananas over these fun facts about bananas!"
    },
    {
        "heading": "Most Korean people don't have armpit odor.",
        "content": "Recent research at the University of Bristol found that only 0.006% of the Korean population has the ABCC11 gene. This gene is the cause of armpit odor.\nIn fact, the study found that most East Asians don't have this gene, but Koreans have the lowest numbers.\nWhile this may be surprising to us, it's not big news in Korea, as deodorant isn't commonly found there!"
    },
    {
        "heading": "The original London Bridge is now in Arizona.",
        "content": "The London Bridge, originally constructed in 1831, was starting to fall apart by the 1960s. As a result, the City of London decided to sell it and build another.\nIn 1963, American entrepreneur Robert P. McCulloch bought the bridge. He dismantled it and shipped it to the United States piece by piece.\nThe bridge moved to Lake Havasu City in Arizona. McCulloch founded Lake Havasu City, and he wanted the bridge to serve as a tourist attraction.\nThe reconstruction took three years to complete. The attraction opened on October 10, 1971, with fireworks, entertainment, and celebrities.\nYou can read more random facts about Arizona here!"
    },
    {
        "heading": "During your lifetime, you will produce enough saliva to fill 50 bathtubs!",
        "content": "The average person produces roughly one ounce (30 ml) of saliva every hour.\nThat's 24.3 ounces (720 ml) or one full wine bottle's worth of saliva a day, which is an average of 69 gallons (263 liters) per year.\nThe average global life expectancy is about 72 years. This means that you produce an average of 4,968 gallons (18,936 liters) of saliva in your lifetime.\nThat's enough to fill 50 bathtubs!"
    },
    {
        "heading": "If Pinocchio said “My Nose Will Grow Now,” it would create a paradox.",
        "content": "As we all know, whenever Pinocchio lies, his nose grows longer.\nBut there's one sentence that Pinocchio could say that breaks this system, which is “my nose will grow now.”\nIf you think about it, Pinocchio's nose would have to grow to make his statement not a lie. But then it can't grow; otherwise, the statement would not be a lie.\nFun Fact: This conundrum is known as the Pinocchio Paradox."
    },
    {
        "heading": "Polar bears could eat as many as 10 penguins in a single sitting…",
        "content": "…If they didn't live at opposite ends of the earth!\nPolar bears live in the Arctic, whereas most common penguins, such as Adélie or emperor penguins live in the south pole.\nThe average adult polar bear weighs 500 pounds (227 kg) and eats about 20% of its total weight each meal. So polar bears can eat about 100 pounds (45 kg) of food in one go.\nAdélie penguins weigh around 10 pounds, so a polar bear would have to eat ten to be full!\nFun Fact: This means that a polar bear could comfortably eat a child!"
    },
    {
        "heading": "Car manufacturer Volkswagen makes sausages.",
        "content": "Most people know Volkswagen for their iconic line of campervans, the Kombi, or even the Beetle.\nA lesser-known product that comes out of Volkswagen's factories is currywurst sausages.\nNow why in the world would Volkswagen make sausages?\nVW built one of their factories in a remote location and decided to make their own food for the factory workers.\nTheir sausages were so popular that Volkswagen ended up selling them commercially.\nFun Fact: Volkswagen's sausages are so popular that they bring in more revenue than their cars!!"
    },
    {
        "heading": "Movie trailers were originally shown after the movie, which is why they're called “trailers.”",
        "content": "The world's first movie trailer was shown at a theater in Harlem, New York, in 1914.\nThe trailer promoted an upcoming movie featuring Charlie Chaplain. The audience would watch the trailer after the movie had ended.\nThe trailers showing after the film was ineffective, as the audience wouldn't stay to watch them."
    },
    {
        "heading": "Hawaiian pizza is a Canadian invention.",
        "content": "First things first, we're not discussing whether ham and pineapple belong on a pizza or not.\nSam Panopoulos emigrated from Greece to Canada in 1954. He became a chef at the Satellite Restaurant in Chatham, Ontario.\nIn 1962, Panopoulos had the idea to add canned pineapple to pizza. Chinese Sweet and sour style cooking was his inspiration for this strange combination.\nThe Hawaiian pizza was unpopular at first due to the unusual fruity ingredient. But, once people tried it, the new topping soon became a common choice worldwide!\nHawaiian pizza has nothing to do with Hawaii. It's actually named after the brand of canned pineapples they originally used."
    },
    {
        "heading": "The smallest bone in your body is in your ear.",
        "content": "Known as the stapes bone, this tiny bone is, on average, 0.09 × 0.11 inches (3 × 2.5 mm) in size.\nThe stapes bone can be found in the middle ear of humans and many other animals.\nIt plays a vital role in transferring vibrations from sounds into the inner ear."
    },
    {
        "heading": "Tennis players can be fined up to $20,000 for swearing while playing at Wimbledon.",
        "content": "It doesn't stop there, though. If players swear once before or during a match, they're fined and given a warning. The second time it happens in one match, they may lose a point.\nOn the third, they may lose a game. Then, finally, they can lose the whole match if they swear four times!"
    },
    {
        "heading": "Only 5% of the ocean has been explored.",
        "content": "The ocean covers around 70% of the Earth's surface, and it is much harder to explore than land.\nAs much as 20% of the ocean floor has now been mapped, thanks to advancements in sonar technologies.\nThe reason we've explored so little of the ocean is that the technology needed has only developed over the last 100 years."
    },
    {
        "heading": "Most people fart around 14 to 23 times a day!",
        "content": "While passing wind may sometimes be embarrassing, it's perfectly natural.\nBy knowing what you eat, you can fart less often and prevent them from being too smelly!\nThe foods most linked to farting include beans, broccoli, milk, and corn. Other high-fiber foods such as fruit, peas, or cabbage can increase the amount of gas you pass."
    },
    {
        "heading": "There is a species of spider called the Hobo Spider.",
        "content": "The hobo spider (Eratigena agrestis) can be found in various places around the world. This includes Europe to Central Asia and parts of western North America.\nThis crafty little critter doesn't live in a standard spider web. Instead, it constructs a funnel made of web in the ground and waits for its prey to stumble into it."
    },
    {
        "heading": "A lion's roar can be heard from 5 miles away.",
        "content": "A lion can roar as loud as 114 decibels, roughly 25 times louder than a gas-powered lawnmower.\nLions can roar louder than other big cats because of the way their vocal cords are shaped. This allows them to produce more noise with less effort."
    },
    {
        "heading": "Saint Lucia is the only country in the world named after a woman.",
        "content": "The island has been continuously inhabited since at least 200 AD but wasn't discovered by Europeans until the 16th Century.\nLegend has it that French sailors were shipwrecked on December 13, 1502, and became stranded on the island.\nAs December 13 is Saint Lucy's Day, they named the island in honor of her.\nIf you're planning a vacation, why not check out these random fun facts about Saint Lucia!"
    },
    {
        "heading": "The national animal of Scotland is a unicorn.",
        "content": "Unicorns have featured in many cultures over the years, going as far back as the middle ages. They're a symbol of purity, innocence, and power in Celtic mythology.\nUnicorns were first introduced to the royal coat of arms of Scotland around the mid-1500s. The unicorn was believed to be the natural enemy of the lion, which is the national animal of England.\nSince the 1707 union of England and Scotland, the royal arms of the United Kingdom include a unicorn and a lion. This displays unity between the two countries.\nBonus Fact: The unofficial national bird of Scotland is the Golden Eagle."
    },
    {
        "heading": "The United States Navy uses Xbox controllers for their periscopes.",
        "content": "In 2018, the US Navy equipped its submarines with Xbox 360 controllers.\nThe control sticks for periscopes are both expensive and difficult to master. So the US Navy began to install Xbox 360 controllers as they are much cheaper.\nIt's not all about cost, though. As many periscope operators have used Xbox controllers in the past, they can easily transfer their skills."
    },
    {
        "heading": "The following can be read forward and backward: Do geese see God?",
        "content": "A palindrome is a word, sentence, or phrase which can be read the same forwards and backward.\nThe word itself is from the Greek words “palin,” meaning “back,” and “dromos,” meaning “direction.”\nPalindromes have been around for thousands of years. The first known palindromes date back to Egypt during the Greek occupation around 300 BC.\nFun Fact: The man credited with writing the first palindromes was executed for writing one that insulted his king!"
    },
    {
        "heading": "A baby octopus is about the size of a flea when it is born.",
        "content": "When an octopus first lays its eggs, they're smaller than a grain of rice. The eggs are so delicate they have to be constantly watched over.\nWhen the baby octopuses emerge from their eggs, they come out fully formed but tiny. They weigh only 0.001 ounces (0.03 grams).\nYou'd think this would make them hard to see, but, since eggs are laid by the tens of thousands, they're easily spotted!"
    },
    {
        "heading": "A sheep, a duck, and a rooster were the first passengers to take a trip in a hot air balloon.",
        "content": "In 1783 the first hot air balloon was launched carrying a sheep, duck, and a rooster.\nThe Montgolfier brothers invented the hot air balloon in France. They began to experiment with balloons after seeing the heat of a fire lift their laundry as it was drying.\nThe inaugural flight took animal passengers as it was unknown how flying at high altitudes would affect people.\nThe flight was a complete success, and the animals landed, safe and mostly unharmed. Although, the sheep managed to land on the rooster."
    },
    {
        "heading": "In Uganda, around 48% of the population is under 15 years of age.",
        "content": "Uganda has a total population of 44.3 million. This means that there are around 20 million people under the age of 15 living there.\nIn total, 77% of the population is under the age of 30. One of the reasons this number is so high is because the population is rapidly expanding. There were just 5 million people in Uganda in 1950."
    },
    {
        "heading": "On average, men get bored of a shopping trip after 26 minutes.",
        "content": "Meanwhile, women don't get tired of shopping until around 2 hours have passed!\nOn top of this, it's been found that eight in ten men hate shopping with their partner.\nMen who are promised a treat at the end of a joint shopping trip are more likely to pretend to enjoy shopping with their partner for longer.\nSo, next time you see a woman at a store with a bored-looking boyfriend, you know they've been out for more than half an hour!"
    },
    {
        "heading": "In the 16th Century, Turkish women could initiate divorce if their husbands didn't provide enough coffee.",
        "content": "This would be unheard of today, but coffee was an integral part of Turkish society back then.\nIt was introduced into the country in the 15th Century, and by the 16th Century, they had mastered the art of coffee.\nCoffee became so popular, it seems, that it became “grounds” for divorce.\nNo one knows why exactly this actually came into law, but the fact remains that it was!"
    },
    {
        "heading": "Recycling just one tin can saves enough energy to watch television for 3 hours.",
        "content": "That's how important recycling is! In fact, recycling an aluminum can into a new one takes only 5% of the energy required to produce one normally.\nThe average person has the chance to recycle 25,000 cans in their lifetime – that's 75,000 hours of television!"
    },
    {
        "heading": "After the premiere of 16 and Pregnant, teen pregnancy rates dropped.",
        "content": "MTV may not have the most wholesome shows, but teen pregnancy dropped by 5.7% within 18 months of the show's premiere.\nWhile this sounds like a success story, the TV show has been criticized for glamourizing teenage pregnancy. Instead of focusing on genuine issues, they focus more on the drama between the parents."
    },
    {
        "heading": "Squirrels cause approximately 10-20% of US power outages.",
        "content": "Harmless and cute as they seem, these fuzzy little creatures aren't as innocent as you think!\nSquirrels tend to chew things, but combine this with power lines, and there's going to be a problem.\nFortunately, squirrel-induced blackouts are much easier to fix. But, let's face it, there's only so much damage one squirrel can do.\nThese blackouts are much smaller than one caused by a storm, as generally, there's just one cable to repair.\nCheck out these other amazing facts about squirrels!"
    },
    {
        "heading": "Facebook, Instagram, and Twitter are all banned in China.",
        "content": "Known as the “Great Firewall of China,” the online restrictions and censorship within its country are expansive.\nOther major banned social network sites include Pinterest and Tumblr. Those aren't the only ones either; over 8,000 domain names are blocked in China.\nThis doesn't mean that people in China can't be social over the internet. There are several popular Chinese-owned and approved social media companies, such as TikTok, Weibo, and WeChat."
    },
    {
        "heading": "95% of people text things they could never say in person.",
        "content": "There's something about saying things over text instead of in person that allows us to speak more honestly. Even if a little too honest at times!\nWhile this often ends up in sticky situations, it has its benefits too…\nPsychologists have found that their patients can open up to them more by texting. They still talk face-to-face with patients, but for some, it can help with their progress."
    },
    {
        "heading": "Honeybees can recognize human faces.",
        "content": "For a long time, we believed that only large-brained mammals could distinguish faces. But the humble honeybee shook that theory up!\nBees can distinguish between many different flowers, so it was theorized that they might tell people apart.\nScientists discovered that honeybees could recognize a familiar face, even days after being trained to do so.\nFun Fact: Bees see faces in a compilation of 5,000 individual images – kind of like pixels."
    },
    {
        "heading": "The Battle of Hastings didn't actually take place in Hastings.",
        "content": "In 1066, the Battle of Hastings was fought between the English forces under King Harold Godwinson and the Norman and French troops under William the Conqueror.\nThe battle is commonly known today as the deciding point in the Norman Conquest of England.\nDespite the name, the actual battle took place 7 miles (11 km) away from Hastings, in a town now known as Battle."
    },
    {
        "heading": "Human blood cells have different lifespans.",
        "content": "Red blood cells circulate the human body for about four months. In comparison, white blood cells range from a few hours to several days.\nPlatelets circulate the body for about nine days. Platelets are cells that circulate our blood, and they bind together when they find damaged blood vessels."
    },
    {
        "heading": "A swarm of 20,000 bees followed a car for two days because their queen was stuck inside.",
        "content": "A 68-year-old grandmother got quite the surprise returning from a nature reserve when a queen bee got trapped in her car.\nShe parked her car to go shopping, and returned to a car covered in bees! The bees were safely removed from the car, and the lovely old lady made her way home.\nMuch to her surprise, the bees were back the next day! It seems that the queen bee was still inside, and the bees followed her the whole way home.\nThis time, they were all removed, and they, fortunately, didn't return!"
    },
    {
        "heading": "Eating carrots can turn your skin orange.",
        "content": "Carrots are full of the natural pigment beta-carotene. This pigment is what gives carrots their vibrant orange color.\nIf you eat an excessive amount of carrots, the beta-carotene can enter your bloodstream. This would give your skin an orange glow!\nThe medical name for this condition is carotenemia. While it's not one of the best things to have, it's generally harmless."
    },
    {
        "heading": "Bob Dylan's birth name was Robert Zimmerman.",
        "content": "When Bob Dylan was fresh out of high school, he chose the stage name Elston Gunn, but this didn't stick for long.\nFor a while, he went by his first and middle name, Robert Allen, but that didn't feel right either.\nEventually, he came upon the name Bob Dylan and officially changed his name to this on August 2, 1962.\nNobody knows why he chose this name, but many people, including Dylan himself, have told different stories over the years."
    },
    {
        "heading": "A crocodile can't poke its tongue out.",
        "content": "Crocodiles cannot stick their tongues out because it's attached to the roof of their mouths.\nWhile this may not seem very practical, it's actually quite convenient for crocodiles. It means that they can't bite their tongues while snapping their powerful jaws together!"
    },
    {
        "heading": "Sea otters hold hands when they sleep so they don't drift away from each other.",
        "content": "While it may look like a couple of otters being adorable, it's actually a life-saving strategy!\nThis technique is most commonly seen with mothers and their pups (that's a baby otter!).\nAnother way they stay still in choppy seas is by grabbing onto long strands of kelp that grow up from the seabed.\nIf you love this fact, check out these 15 otterly awesome facts about otters!"
    },
    {
        "heading": "A small child could swim through the veins of a blue whale.",
        "content": "We all know blue whales are enormous, but this puts it into a whole new perspective!\nThe largest animals on the planet, blue whales, can grow as large as 100 feet (30 m) long and weigh up to 150 tons (152,407 kg).\nTheir hearts are obviously huge too, about the same size as a small car.\nSo it's no surprise that a child of three or four could swim with ease through a blue whale's massive veins!"
    },
    {
        "heading": "The word “y'all” dates back to at least 1631.",
        "content": "Whether you like it or not, the shortening of “you all” to “y'all” is here to stay.\nFor a long time, people believed the term originated sometime in the 18th or 19th centuries, but in fact, it's been in use for much longer.\nIn 1631, English scholar William Lisle wrote the following in a book on Ethiopian history:\n“The captive men of strength I gave to you, the weaker sold, and this y'all know is true.”"
    },
    {
        "heading": "J.K. Rowling chose the unusual name “Hermione” so young girls wouldn't be teased for being nerdy.",
        "content": "J.K Rowling came upon the name Hermione from a character in William Shakespeare's “A Winter Night's Tale.”\nRowling wanted to use a name that wasn't commonly used. She said that when choosing the name, she “didn't want a lot of fairly hard-working little girls to be teased if ever the book was published.”"
    },
    {
        "heading": "Hewlett-Packard's (also known as HP) name was decided in a coin toss in 1939.",
        "content": "Bill Hewlett and Dave Packard met in the early 1930s while studying Engineering. Several years later, they started their own company, operating from a tiny garage.\nIn 1939 they cemented their partnership and decided on the company's name. It would simply be the hyphening of their two surnames.\nTo decide on the order in which their names would be presented, they flipped a coin. The winner would give the final choice.\nDave Packard won the coin toss, but he preferred how Hewlett-Packard sounded, so they stuck with that!\nYou may also like these top 100 fun facts about technology."
    },
    {
        "heading": "There are a total of 1,710 steps in the Eiffel Tower.",
        "content": "Standing at 108 stories tall, the Eiffel Tower is one of Europe's most iconic landmarks.\nThe Eiffel Tower was constructed in 1889, and until 1930 it was the tallest building in the world. So it's no surprise that it's often found on people's bucket lists!\nTo reach the top of this 1,063 feet (324 m) tall marvel, you must climb 1,710 steps. However, guests are only allowed to climb the stairs until the first platform. From there, they must take an elevator to the top."
    },
    {
        "heading": "The names of the Pokémon Hitmonlee and Hitmonchan are based on Bruce Lee and Jackie Chan.",
        "content": "The two fighting-style Pokémon Hitmonlee and Hitmonchan have been present within the games since their debut on Gameboy.\nAs Pokémon is a Japanese creation, the original names of most creatures were quite different.\nWhen Pokémon was introduced to the western world, their names were also westernized. So these Pokémon were named after internationally famous martial artists.\nThe third Pokémon of the Hitmons, Hitmontop, is also named after a martial artist – Larry Top.\nIf you love Pokémon, you'll love this list of fun facts about the original 151 Pokémon."
    },
    {
        "heading": "Pigs are considered to be the world's fifth-smartest animal.",
        "content": "Ah, pigs. They roll around in muck and filth, eat any scraps left around for them, and for some, are quite delicious.\nThat's not all, though; it turns out that they're incredibly intelligent!\nPigs can solve puzzles better than chimpanzees, and they have some of the best long-term memories known in animals."
    },
    {
        "heading": "Pirates wore earrings because they believed they improved their eyesight.",
        "content": "In fact, there are many reasons why pirates wore earrings…\nSome pirates would use trinkets for earrings from faraway lands. This was to show how well-traveled they were.\nPirates believed that the precious metals in their earrings were magical and it would protect or enhance their eyesight.\nAlso, pirates believed earrings could aid in seasickness and prevent them from drowning."
    },
    {
        "heading": "Los Angeles original name is “El Pueblo de Nuestra Senora la Reina de Los Angeles de Porciuncula.”",
        "content": "Spanish colonists founded the city that is now known as Los Angeles in 1769. And in 1781, another group of 44 settlers made the new town their home.\nThe Spanish governor named the city, El Pueblo de Nuestra Señora la Reina de los Ángeles de Porciúncula. In English, this means, “The Town of Our Lady the Queen of the Angels of Porciúncula”.\nAs the name is quite a mouthful, it became shortened until it finally became Los Angeles. So now, Los Angeles is just “The Angels.”"
    },
    {
        "heading": "The Twitter bird actually has a name – Larry.",
        "content": "When Twitter was founded in 2006, its logo was purchased from a stock image website. The bird logo has had small changes to its appearance in the years since.\nIt wasn't until the 2010s that a Twitter employee revealed that it's actually called Larry.\nTwitter has since confirmed this and stated that the name comes from Larry Bird, who is a famous Hall of Fame basketball player.\nThe species of Larry the Bird remains a secret!"
    },
    {
        "heading": "Octopuses actually have six arms and two legs!",
        "content": "Animals that walk on two appendages use their bottom two for walking and the top two for manipulating objects.\nIt seems that octopuses also similarly favor some of their tentacles.\nSix of an octopuses tentacles are used in the same way we would use our arms and are used for purposes such as eating.\nOctopuses use their remaining two tentacles for walking, making them just like legs.\nUnlike humans, octopuses do not favor one side over the other. So for an octopus, there's no such thing as being left or right-tentacled!"
    },
    {
        "heading": "Pound cake got its name because the original recipe contained a pound of butter, sugar, flour, and eggs.",
        "content": "The simple measurements made the recipe easy to remember. Few people could read back then, so an easy-to-remember recipe was key.\nOne pound of each ingredient would've made the cake big enough to feed multiple families.\nThe portions were adjusted over time, to make the cakes smaller and lighter, but the name stayed the same.\nBonus Fact: The German chocolate cake has nothing to do with Germany. A Texan invented the cake and used baking chocolate named after the creator, Sam German."
    },
    {
        "heading": "There are only two times that we know of that snow fell in the Sahara desert.",
        "content": "February 18, 1979, was a special day for residents of Ain Sefra, a town in Algeria at the edge of the Sahara desert.\nIt was special because it was the first time snow could be seen falling in the Sahara desert for as long as anyone can remember.\nIt snowed for 30 minutes before the average temperature rose, and the snow rapidly melted.\nSince then, there has been just one case of it happening again, on December 19, 2016."
    },
    {
        "heading": "Mike Tyson once offered a zoo attendant $10,000 to let him fight a gorilla.",
        "content": "Back in the 90s, Mike Tyson was a true force to be reckoned with. Tyson had already bribed a zoo attendant to open the zoo just for himself and his then-wife, Robin Givens.\nIt was during this visit that he made his outlandish request. He demanded the attendant “to open the cage and let me smash that silverback's snot box.”\nFortunately for everyone involved, the zoo attendant declined his request."
    },
    {
        "heading": "ABBA turned down 1 billion dollars to do a reunion tour.",
        "content": "At the height of their success in 1979, ABBA was one of the biggest pop bands in the world.\nThree years later, the group split up following the divorce of two of their members.\nIn 2000, ABBA was offered $1 billion to reunite for 100 shows – which would have been $250 million per member.\nWhen asked why they wouldn't accept the offer, they simply said, “it's a hell of a lot of money to say no to, but we decided it wasn't for us.”"
    },
    {
        "heading": "Abraham Lincoln fed his cat with a gold fork.",
        "content": "Abraham Lincoln was known to be a lover of animals, but his love for cats was next level!\nThe Lincoln family often ate at the White House dinner table with their cat, Tabby. And during a formal dinner at the White House, Abe Lincoln fed Tabby from the table with a gold fork.\nLincoln's embarrassed wife said it was “shameful in front of their guests.”\nThe president replied, “If the gold fork was good enough for former President James Buchanan, I think it is good enough for Tabby.”"
    },
    {
        "heading": "The first alarm clock could only ring at 4 am.",
        "content": "While alarms and clocks have been around for a long time, combining the two is a much more recent invention!\nLevi Hutchins created the first mechanical alarm clock in 1787. He did so as he was determined to wake up at 4 am – before sunrise – no matter what day it was.\nHis invention worked perfectly, for him at least. He was so happy, in fact, that he never patented his device or sold it commercially.\nIt took another 60 years for a wind-up alarm clock to be invented to be set to any time."
    },
    {
        "heading": "Some insects and small birds see the world in slow motion.",
        "content": "This is because they can take in more information per second than other, larger animals.\nIt allows them to move rapidly and with precision, which is vital to escape from predators.\nThey process information so quickly that they perceive time as though it was in slow motion.\nFun Fact: It's the opposite for some larger animals. For example, elephants take a lot more time to absorb information and act upon it."
    },
    {
        "heading": "A goat called William Windsor served as a Lance Corporal in the British Army.",
        "content": "William “Billy” Windsor I served in the 1st Battalion Infantry Unit of The Royal Welsh between 2001 & 2009.\nBilly was not the only animal and will certainly not be the last to serve in the Royal Welsh, as the tradition dates back to 1844.\nFollowing Billy's retirement, he was replaced by a younger goat named William Windsor II."
    },
    {
        "heading": "The most venomous jellyfish in the world is the Irukandji.",
        "content": "The Irukandji are a few different species of box jellyfish commonly found in the waters off Australia's coast.\nDespite being the most venomous jellyfish in the world, they're not the most dangerous.\nThe more lethal species of jellyfish are also box jellyfish but are larger and can administer their venom much faster.\nDespite this, you should avoid the Irukandji at all costs, which is rather tricky as they're smaller than your fingernail!\nAnother reason to steer clear is that their venom is 100 times more potent than a cobra's."
    },
    {
        "heading": "March 20th is known as Snowman Burning Day.",
        "content": "Snowman Burning Day was first celebrated on March 20, 1971, at Lake Superior State University in Michigan.\nThe Rose Sunday Festival inspired this bizarre-sounding celebration in Germany.\nIn the original Rose Sunday Festival, a parade passed through town, and the mayor would make an agreement with the town's children.\nIf they promise to be well behaved and study well that year, then he would order a “snowman” made out of straw to be burned."
    },
    {
        "heading": "Queen Elizabeth II can't sit on the Iron Throne from Game of Thrones.",
        "content": "Queen Elizabeth II visited the Game of Thrones set, but she couldn't sit on it because of an obscure rule.\nAn old and relatively irrelevant rule states, “the ruling monarch can't sit on a foreign throne.”\nDespite this throne being a work of fiction, the queen is a stickler for rules and declined to sit on the Iron Throne!"
    },
    {
        "heading": "There is an official Wizard of New Zealand.",
        "content": "In 1990, the Prime Minister of New Zealand appointed Ian Brackenbury Channell, an old friend, as the official Wizard of New Zealand.\nHe is even given an annual stipend. Known simply as “The Wizard,” he is quite outspoken on social issues.\nHe was even given the Queen's service medal for his lifelong service to the community."
    },
    {
        "heading": "An apple, potato, and onion taste the same if you eat them with your nose plugged.",
        "content": "At least 80% of our sense of taste comes from our sense of smell.\nBecause of this, if you were to block the sense of smell, many foods would taste the same, or at least pretty close.\nIn this case, it was tested on many different people who were blindfolded and had their noses plugged.\nThe results? The participants couldn't distinguish between the three, other than from their texture!"
    },
    {
        "heading": "The longest word you're likely to encounter on an everyday basis is “uncharacteristically.”",
        "content": "At 20 letters long, uncharacteristically is far from the longest word in the English language.\nHowever, a study of 1.7 million samples of everyday English found that it's the longest you're likely to encounter on a daily basis."
    },
    {
        "heading": "A company in Poland makes dinnerware out of wheat so that you can eat your plate!",
        "content": "They make plates out of wheat bran because it's not just edible; it's completely biodegradable too! Say goodbye to feeling guilty about using disposable dinnerware!\nPlastic dinnerware can take centuries to decompose, but it takes just thirty days when made from wheat bran.\nThe company makes plates, bowls, and even cutlery that can withstand high temperatures and wet foods. Unfortunately, the dinner table isn't edible."
    },
    {
        "heading": "The average person walks the equivalent of five times around the world in their lifetime.",
        "content": "Unless you're a bit of a couch potato, you will, on average, walk around 7,500 steps per day.\nThe average person lives until they're 80, so it works out that you'll walk about 110,000 miles (177,027 km) in your lifetime.\nThe circumference of the Earth at the equator is 24,900 miles (40,072 km).\nProviding you're an average person, who takes average strides and lives an average length of time, it's entirely possible to walk the globe five times!"
    },
    {
        "heading": "Michael Jackson offered to make a Harry Potter musical, but the offer was rejected.",
        "content": "Michael Jackson, like many others around the world, was a bit of a Potterhead. He saw the opportunity to turn the books into a musical and pitched the idea to J.K Rowling.\nFor better or worse, Rowling didn't see it as something that would be incredible and rejected it.\nIn an interview with Oprah Winfrey, Rowling defended her decision, saying she “turned down many adaption opportunities, and Michael Jackson's just so happened to be one of them.”"
    },
    {
        "heading": "The world record for stuffing drinking straws into your mouth at once is 650.",
        "content": "On August 25, 2018, Nataraj Karate broke the Guinness World Records for stuffing 650 drinking straws in his mouth at once!\nKarate broke the world record in Tamil Nadu, India, making him the second Indian in a row to break the world record.\nHe had to keep the straws in his mouth for at least 10 seconds to break the record.\nThis makes the seventeenth time that this record has been broken so far!"
    },
    {
        "heading": "Nutella was invented shortly after WWII ended because chocolate was so expensive.",
        "content": "The availability of chocolate was low around this time because most of the world's armies issued rations of chocolate to their soldiers. The lack of supply led many to try creative new approaches.\nIn 1946 Pietro Ferrero created a spread made of tiny amounts of chocolate and plenty of inexpensive hazelnuts.\nAlthough it wasn't a new idea, his formula was, making it much more affordable to regular folk!\nFerrero's son created the final Nutella product and perfected the formula in 1964."
    },
    {
        "heading": "North Korea has its own space program.",
        "content": "The North Korea Space Program gained international attention in 1998 when a satellite launch failed to reach orbit.\nThere have been four launches since, with the latest taking place in 2016.\nThe two satellites which actually reached orbit both failed to function. However, according to North Korea, all launches have been great successes."
    },
    {
        "heading": "According to Genesis 1:20-22, the chicken came before the egg.",
        "content": "The age-old question seems to have been finally answered, and who answered it? The Bible!\nThe Book of Genesis states that “God created all living things.” It even specifies that he created all birds and instructed them to go out and increase in number.\nHow do birds increase in number, you may ask? By laying eggs! Now, this fact only holds up if you believe in God, but it's still a pretty great answer!"
    },
    {
        "heading": "Ants leave maps for other ants when they walk.",
        "content": "Ants leave trails of pheromones when they walk as maps for other ants to follow. This means they can travel the fastest route to sources of food or their hive.\nThe more ants that walk that route, the stronger the map is for others to follow. So even if a few ants get temporarily lost, they'll generally find their way home.\nThe amazing thing is that the ants don't smell the pheromones but detect them with their antennae!"
    },
    {
        "heading": "Tears contain a natural painkiller, which reduces pain and improves your mood.",
        "content": "The next time you find yourself close to tears, don't hold back and just let it all out!\nThe explanation comes down to the fact that emotional tears contain endorphins.\nEndorphins are our body's natural painkillers and mood-improvers."
    },
    {
        "heading": "Saturn is the only planet in our solar system that could float in water.",
        "content": "Although Saturn is the second-largest planet in our solar system, it's also the lightest.\nSaturn could float in water because it's basically a giant gas ball. However, the true fact here is that you'd need an enormous bathtub!\nFun Fact: One year on Saturn is equivalent to 29.457 Earth years, or 10,759 Earth days."
    },
    {
        "heading": "Male cats have longer tails than female cats.",
        "content": "Male cats have longer tails simply because they are, on average, larger than female cats.\nCats' tails are generally proportional to their body, so a larger body means a larger tail.\nOn average male cats' tails measure around 11 inches (28 cm), whereas the female cats' tails are about 9.9 inches (25 cm) long!\nIf you're enjoying these facts so far, you'll love our list of 100 fun facts about cats!"
    },
    {
        "heading": "Dolly Parton lost in a Dolly Parton look-alike contest.",
        "content": "Dolly Parton once entered a Dolly Parton-themed drag queen contest and was quite surprised by the result.\nMany of the participants had spent months or even years fine-tuning their costumes and makeup. But Parton decided to enter in the spur of the moment.\nShe did her hair and makeup more dramatically than usual. She not only lost but ended up receiving the least applause!\nFun Fact: Dolly Parton said that she would likely have done drag if she were born a man!"
    },
    {
        "heading": "George W. Bush was once a cheerleader.",
        "content": "What's most surprising about this fact is that George W. Bush wasn't the only US president to have been a cheerleader in his youth!\nIn 1963 he attended Phillips Academy in Andover, Massachusetts.\nDuring the school year, he was photographed wearing a short skirt and false breasts stuffed down his sweater to cheer on his school's team.\nWhile this was actually intended to mock the other school's team, it makes for a great, true story!"
    },
    {
        "heading": "In total, there are 205 bones in the skeleton of a horse.",
        "content": "While horses may be much larger than us, they have only one less bone than us, with the human body having 206 bones.\nWe suppose this only leaves us with one question: What bone do we have that horses don't?\nYou may also like these 30 fun facts about horses."
    },
    {
        "heading": "Coca-Cola once bought all the website URLs that can be read as ahh, all the way up to 62 h's.",
        "content": "In 2013, the soft drink company tried to win over millennials with a digital campaign.\nCoca-Cola created websites full of animated games, interactive gifs, and videos.\nThe “ahh” in the URL stands for “the sound a smile would make if it made sounds.”\nWhile their ad campaign ended up being a huge success, the websites have since been deactivated.\nYou can read more crazy facts about Coca-Cola here!"
    },
    {
        "heading": "Each year there are more than 40,000 toilet-related injuries in the US.",
        "content": "It may come as a bit of a shock to you, but injuries of this sort are much more common than you'd think!\nSome injuries wouldn't win a Nobel Prize, such as children falling off the toilet.\nBut then there are other funny incidents, like the toilet physically collapsing due to the person's weight sitting on it."
    },
    {
        "heading": "Strawberries can be red, yellow, green, or white.",
        "content": "This doesn't just include the different maturity stages of a strawberry, though, but let's talk about that first.\nMost people only experience strawberries when they're already picked and packed into punnets. However, strawberries aren't red when they start growing.\nInstead, they start green and turn to red as they ripen.\nYellow or white strawberries, on the other hand, are an entirely different species of strawberries!"
    },
    {
        "heading": "Walt Disney World is the second-largest buyer of fireworks in the US.",
        "content": "While this fact may seem shocking at first, it's no real surprise when you look deeper into it.\nThere are six Walt Disney World's in total, and most of them have nightly fireworks displays.\nSome shows cost up to $50,000, so Disney World spends at least $50 million on fireworks over the course of a year!"
    },
    {
        "heading": "Four people lived in a home for six months infested with over 2,000 venomous spiders.",
        "content": "When the Barger family moved into an old limestone house in Kansas City, they had no idea what they were getting themselves into.\nThey saw a few spiders, but they didn't start paying attention until they came upon a highly venomous spider.\nThe brown recluse spider is claimed to be the cause of tens of thousands of bites yearly.\nOver six months, the Barger's spent up to two hours every night searching for them. As a result, they collected 2,055 brown recluse spiders, capturing 37 spiders in just one night!\nIt turns out that brown recluse spiders are not anywhere near as harmful as they're claimed to be, as they weren't bitten even once!"
    },
    {
        "heading": "Madonna has brontophobia, which is the fear of thunder.",
        "content": "While it may sound like a fear of brontosauruses, the word “bronto” comes from the Ancient Greek word meaning thunder.\nAnyway, Madonna's fear is a genuine and often crippling condition.\nIn fact, she's so scared of thunder and lightning that she demands weather reports before her shows.\nFun Fact: The fear of thunder is also known as astraphobia, astrapophobia, keraunophobia, or tonitrophobia."
    },
    {
        "heading": "In June 2017, the Facebook community reached 2 billion active users.",
        "content": "This was quite the milestone for the social network, as it doubled in size in a five-year period!\nSince then, Facebook's growth has slowed dramatically. The social network had around 2.6 billion active users in 2020.\nSo that's more than one-third of the world's population checking their Facebook on a regular basis."
    },
    {
        "heading": "Samuel L. Jackson requested a purple lightsaber in Star Wars to accept the part as Mace Windu.",
        "content": "Samuel L. Jackson is a bit of a self-professed geek, so it was no surprise that he asked George Lucas to cast him in the prequels.\nJackson wanted to find himself on screen in big fight scenes, so he made a special request to Lucas.\nLucas initially declined, stating that lightsabers could only be blue, green, or red. But, fortunately for fans of the purple lightsaber, he eventually changed his mind!"
    },
    {
        "heading": "Paraskavedekatriaphobia is the fear of Friday the 13th.",
        "content": "Friday the 13th is considered unlucky within the Western culture, with roots going back to Norse mythology.\nIt was established by the 20th Century that any Friday which happened to fall on the 13th of any month would inherently be full of misfortune.\nThe phobia itself is connected to Triskaidekaphobia, which is the fear of the number 13."
    },
    {
        "heading": "Kleenex tissues were originally used as filters in gas masks.",
        "content": "The Kleenex brand is part of a larger company, Kimberly-Clark, which started as a paper mill in the late 19th Century.\nWith the first large-scale use of gas in warfare during WWI, there was suddenly a severe demand for a solution.\nEnter the Kleenex tissue, a newly developed thin cotton-like material made from wood pulp.\nOne of the first uses of the tissue was as a replaceable filter in gas masks, making it a life-saving invention!"
    },
    {
        "heading": "In 1998, Sony accidentally sold 700,000 camcorders that could see through people's clothes.",
        "content": "Sony designed the cameras to capture footage better in the dark. So their mistake was actually innocent.\nThe camcorders were able to see through clothes as they had the ability to record in infra-red. But during the day, you could see through someone's outer layer of clothing!\nAs soon as Sony realized their error, they attempted to recall all the cameras, making it their largest product recall to date."
    },
    {
        "heading": "During your lifetime, you will spend around seventy-nine days brushing your teeth.",
        "content": "It's common practice to brush your teeth twice a day, for two minutes at a time.\nFour minutes of brushing a day over a year is 1,460 minutes, which is just over one day of tooth brushing every year.\nSo, if you live for the average life expectancy in the US, 79 years, you'll brush your teeth for seventy-nine days in total!\nThis is based on the recommended time you should be brushing your teeth for – which you are doing, right?\nHere are some cool facts on how much time people spend doing stuff in their lifetime."
    },
    {
        "heading": "Ronald McDonald is “Donald McDonald” in Japan because it makes pronunciation easier for the Japanese.",
        "content": "When McDonald's opened their first restaurant in Japan, they realized they had a problem.\nThe letters “R” and “L” in English are rather tricky for Japanese speakers to pronounce.\nAs such, McDonald's decided it would be easier for all if they changed their mascot's name to “Donaudo Makudonarudo,” or Donald McDonald.\nWhat do they call the Hamburglar, you may ask? Hanbaaguraa!"
    }
]


def get(count=1, include_details=True):
    '''
    Returns a fun fact from The Fact Site (thefactsite.com)
    '''

    # Sample `count` number of data
    random_fun_facts = random.sample(fun_facts, count)

    # Keep only heading if `include_details=False`
    if not include_details:
        random_fun_facts = [{"heading": fact["heading"]}
                            for fact in random_fun_facts]

    return random_fun_facts


if __name__ == "__main__":
    fact = get()
    print(fact[0]['heading'])
    print("\n"+fact[0]['content'])
