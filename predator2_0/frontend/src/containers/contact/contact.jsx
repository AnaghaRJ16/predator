import React from "react";
import "./contanct.css";
import logo from "../../assets/logo.png"; 

const Contact = () => {
  return (
    <div className="gpt3__footer section__padding">
      <div className="gpt3__footer-heading">
        <h1 className="gradient__text">
            Do you want to explore more features?

        </h1>
      </div>
      <div className="gpt3__footer-btn">
        <p>CONTACT US</p>
      </div>
      <div className="gpt3__footer-links">
        <div className="gpt3__footer-links_logo">
          <img src={logo} alt="GPT-3 logo" /> 
          <p>PREDATOR 2.0 , All Rights Reserved</p>
        </div>
        <div className="gpt3__footer-links_div">
          <h4>Links</h4>
          <p>Overons</p>
          <p>Social Media</p>
          <p>Counters</p>
          <p>Contact</p>
        </div>
        <div className="gpt3__footer-links_div">
          <h4>Company</h4>
          <p>Terms & Conditions</p>
          <p>Privacy Policy</p>
          <p>Contact</p>
        </div>
        <div className="gpt3__footer-links_div">
          <h4>Get in touch</h4>
          <p>Anagha RJ</p>
          <p>91 2358132567</p>
          <p>info@payus.net</p>
        </div>
      </div>
      <div className="gpt3__footer-copyright">
        <p>©All rights reserved.</p>
      </div>
    </div>
  );
};

export default Contact;
