// Auto-generated. Do not edit!

// (in-package rover_20_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Arm_msgs {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.joint0 = null;
      this.joint1 = null;
      this.joint2 = null;
      this.joint3 = null;
      this.joint4 = null;
      this.joint5 = null;
      this.joint6 = null;
    }
    else {
      if (initObj.hasOwnProperty('joint0')) {
        this.joint0 = initObj.joint0
      }
      else {
        this.joint0 = 0.0;
      }
      if (initObj.hasOwnProperty('joint1')) {
        this.joint1 = initObj.joint1
      }
      else {
        this.joint1 = 0.0;
      }
      if (initObj.hasOwnProperty('joint2')) {
        this.joint2 = initObj.joint2
      }
      else {
        this.joint2 = 0.0;
      }
      if (initObj.hasOwnProperty('joint3')) {
        this.joint3 = initObj.joint3
      }
      else {
        this.joint3 = 0.0;
      }
      if (initObj.hasOwnProperty('joint4')) {
        this.joint4 = initObj.joint4
      }
      else {
        this.joint4 = 0.0;
      }
      if (initObj.hasOwnProperty('joint5')) {
        this.joint5 = initObj.joint5
      }
      else {
        this.joint5 = 0.0;
      }
      if (initObj.hasOwnProperty('joint6')) {
        this.joint6 = initObj.joint6
      }
      else {
        this.joint6 = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Arm_msgs
    // Serialize message field [joint0]
    bufferOffset = _serializer.float64(obj.joint0, buffer, bufferOffset);
    // Serialize message field [joint1]
    bufferOffset = _serializer.float64(obj.joint1, buffer, bufferOffset);
    // Serialize message field [joint2]
    bufferOffset = _serializer.float64(obj.joint2, buffer, bufferOffset);
    // Serialize message field [joint3]
    bufferOffset = _serializer.float64(obj.joint3, buffer, bufferOffset);
    // Serialize message field [joint4]
    bufferOffset = _serializer.float64(obj.joint4, buffer, bufferOffset);
    // Serialize message field [joint5]
    bufferOffset = _serializer.float64(obj.joint5, buffer, bufferOffset);
    // Serialize message field [joint6]
    bufferOffset = _serializer.float64(obj.joint6, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Arm_msgs
    let len;
    let data = new Arm_msgs(null);
    // Deserialize message field [joint0]
    data.joint0 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [joint1]
    data.joint1 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [joint2]
    data.joint2 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [joint3]
    data.joint3 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [joint4]
    data.joint4 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [joint5]
    data.joint5 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [joint6]
    data.joint6 = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 56;
  }

  static datatype() {
    // Returns string type for a message object
    return 'rover_20_control/Arm_msgs';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4515360d2b590c5a38f3e5678e7e9266';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64  joint0
    float64 joint1
    float64 joint2
    float64  joint3
    float64  joint4
    float64  joint5
    float64  joint6
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Arm_msgs(null);
    if (msg.joint0 !== undefined) {
      resolved.joint0 = msg.joint0;
    }
    else {
      resolved.joint0 = 0.0
    }

    if (msg.joint1 !== undefined) {
      resolved.joint1 = msg.joint1;
    }
    else {
      resolved.joint1 = 0.0
    }

    if (msg.joint2 !== undefined) {
      resolved.joint2 = msg.joint2;
    }
    else {
      resolved.joint2 = 0.0
    }

    if (msg.joint3 !== undefined) {
      resolved.joint3 = msg.joint3;
    }
    else {
      resolved.joint3 = 0.0
    }

    if (msg.joint4 !== undefined) {
      resolved.joint4 = msg.joint4;
    }
    else {
      resolved.joint4 = 0.0
    }

    if (msg.joint5 !== undefined) {
      resolved.joint5 = msg.joint5;
    }
    else {
      resolved.joint5 = 0.0
    }

    if (msg.joint6 !== undefined) {
      resolved.joint6 = msg.joint6;
    }
    else {
      resolved.joint6 = 0.0
    }

    return resolved;
    }
};

module.exports = Arm_msgs;
