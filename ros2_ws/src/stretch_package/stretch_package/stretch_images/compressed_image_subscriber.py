import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from rclpy.wait_for_message import wait_for_message
import cv2
from cv_bridge import CvBridge

class CompressedImageSubscriber(Node):
    
    def __init__(self, vis=False):
        super().__init__('compressed_image_subscriber_node')
        self.bridge = CvBridge()
        self.vis = vis
        self.image = None
        
        self.get_logger().info('Waiting for messages on topic: /camera/color/image_raw/compressed')
        try:
            _, msg = wait_for_message(CompressedImage, self, '/camera/color/image_raw/compressed')
            if msg is not None:
                self.get_logger().info('CompressedImage message received!')
                self.process_image(msg)
        except Exception as e:
            self.get_logger().error(f'Error waiting for image: {e}')

    
    def process_image(self, msg):
        try:
            self.image = msg
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')
            self.get_logger().info('Converted CompressedImage message to OpenCV Image.') 
            image_path = '/home/ws/data/images/head_image.png'
            cv_image = cv2.rotate(cv_image, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(image_path, cv_image)
            self.get_logger().info(f'Image saved at {image_path}')
            if self.vis:         
                cv2.imshow('Compressed Image', cv_image)
                cv2.waitKey(0)  # Wait indefinitely until a key is pressed
                self.get_logger().info('Key pressed, closing the image window.')
        except Exception as e:
            self.get_logger().error(f'Error converting image: {e}')
        

def main(args=None):
    rclpy.init(args=args)
    node = CompressedImageSubscriber()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

