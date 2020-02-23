<?php


$conn = mysqli_connect(
    "localhost",
    "root",
    "",
    "maldatabase"
);

extract($_POST);
if(isset($_POST['kon'])){

    $data ="";
    $result = mysqli_query($conn,'SELECT * FROM table1 ORDER BY id DESC');

    $b = array();


    if(mysqli_num_rows($result)>0){
        $data .="<div class='row'>";
        while($row  = mysqli_fetch_array($result)){
            array_push($b,$row['result']);
            $data .="
            <div class='col-4 mb-5 mt-5'>
            <div class='card bg-light shadow' style='height: auto;'>
            <img src='./cropped_images/".$row['image_name']."' class='card-img-top img-thumbnail' alt=''>
            <div class='card-body '>
            <hr>Detection result: ".$row['result']."
            <hr>Image name : ".$row['image_name']."
            <br>
            </div>
            </div>
            </div>";
        }
        $data .="</div>";

    }
    else{
        $data .="<center><h4 class='text-danger'>Oops ! <span class='text-dark'>No Data Found.</span></h4></center>";
    }


    echo $data;
}
?>
