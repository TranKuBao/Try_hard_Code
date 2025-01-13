<!DOCTYPE html>
<html>
<body>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER("PHP_SELF"))?>">
        Name: <input type="text" name="name"><br>
        E-mail: <input type="text" name="email"><br>
        Website: <input type="text" name="website"><br>
        Comment: <textarea name="comment" rows="5" cols="40"></textarea><br>
        <input type="submit">
    </form>

    <?php
        // Process the form data when the form is submitted
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $name = $_POST["name"];
            $email = $_POST["email"];
            $website = $_POST["website"];
            $comment = $_POST["comment"];
            $nameErr="";
            // Add your processing logic here
            // For example, you can echo or use the data as needed
            if (empty($_POST["name"])) {
                $nameErr = "Name is required";
                echo "Name: $nameErr";
              } else {
                $name = test_input($_POST["name"]);
                // check if name only contains letters and whitespace
                if (!preg_match("/^[a-zA-Z-' ]*$/",$name)) {
                  $nameErr = "Only letters and white space allowed";
                  echo "Name: $nameErr";
                }
              }

            echo "E-mail: $email<br>";
            echo "Website: $website<br>";
            echo "Comment: $comment<br>";
        }

    ?>

</body>
</html>
