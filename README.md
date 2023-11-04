# PhotoShotMax
An entry-level kiosk interface to enable live photo sharing over email during a photo shoot or photobooth.


This short project was started on 11/3/2023 for a Seattle University A.n.I.Ma.L club and ACM club **headshot and networking event**. The first major version was finished on the same day.



---

<br>

**Here is how the program works:**

1. Take pictures using a camera connected to your computer or mount a camera file system.

2. This program watches the folder your pictures are stored to, the "source" folder, and displays the latest picture live.

3. At the same time, this program prompts users for their contact information in a terminal window.

4. After a user enters their contact information. The program renames the picture with the user's email and copies it into a second "target" watched folder.

5. The "target" folder is stored in OneDrive, and uses a simple Power Automate script to send an email with any uploaded files as an attachment.


<br>


**To use this program**:

1. Download this program and install the OpenCV Package:

    ``pip install opencv-python``

2. Update the "source" watched folder that receives images from the camera and the "target" watched folder that is connected to Power Automate or another automation tool.

3. Update the questions, question types, and summary labels in a way that works best for your data.

4. Run the program and add pictures to the watched folder.

5. Watch your users smile as they receive their pictures in real-time!
