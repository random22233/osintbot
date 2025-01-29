import { InstagramOutlined } from "@ant-design/icons";
import { FaLinkedinIn } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";

const Footer = () => {
  return (
    <footer
      className="bg-gray-900 text-gray-400 py-2 fixed bottom-0 w-[100%] px-10 text-sm"
      style={{ borderTop: "1px solid rgb(51 65 85)" }}
    >
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
        <div className="flex items-center justify-between gap-5">
          {/* Left Section */}
          <div className="flex items-center space-x-2">
            <span>Made by</span>
            <a href="#" className="text-teal-400 hover:underline font-semibold">
              Predicta Lab
            </a>
          </div>

          {/* Center Section */}
          <div className="flex space-x-2 mt-4 md:mt-0 items-center">
            <a
              href="#"
              className="text-gray-400 hover:text-gray-200"
              aria-label="Twitter"
            >
              <FaXTwitter />
            </a>
            <a
              href="#"
              className="text-gray-400 hover:text-gray-200"
              aria-label="Instagram"
            >
              <InstagramOutlined />
              {/* Use an icon library like Font Awesome */}
            </a>
            <a
              href="#"
              className="text-gray-400 hover:text-gray-200"
              aria-label="LinkedIn"
            >
              <FaLinkedinIn />
            </a>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex flex-wrap justify-center mt-4 md:mt-0 md:justify-end space-x-4 text-teal-400">
          <a href="#" className="hover:text-teal-400">
            FAQ
          </a>
          <a href="#" className="hover:text-teal-400">
            Terms and conditions
          </a>
          <a href="#" className="hover:text-teal-400">
            Legal notice
          </a>
          <a href="#" className="hover:text-teal-400">
            Data protection policy
          </a>
          <a href="#" className="hover:text-teal-400">
            Code of ethics
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
