import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class EdgeDetectionNode(Node):
    def __init__(self):
        super().__init__('edge_detection_node')
        self.subscription = self.create_subscription(
            Image,
            '/camera',
            self.listener_callback,
            10
        )
        self.publisher = self.create_publisher(
            Image,
            '/camera/edges',
            10
        )
        self.cv_bridge = CvBridge()
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Receiving video frame')
        # Convert ROS Image message to OpenCV image
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")

        # Apply Canny edge detection
        edges = cv2.Canny(cv_image, 100, 200)

        # Convert OpenCV image to ROS Image message
        edge_img_msg = self.cv_bridge.cv2_to_imgmsg(edges, "mono8")

        # Publish the edge-detected image
        self.publisher.publish(edge_img_msg)

def main(args=None):
    rclpy.init(args=args)

    edge_detection_node = EdgeDetectionNode()

    rclpy.spin(edge_detection_node)

    # Destroy the node explicitly
    edge_detection_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
