using System;
using System.Linq;
using System.Threading;
using SharpDX.DirectInput;
using Nefarius.ViGEm.Client;
using Nefarius.ViGEm.Client.Targets;

namespace DpadStickToggle
{
    public class DpadMapper
    {
        private readonly DirectInput _directInput;
        private Joystick _joystick;
        private Xbox360Controller _xbox;
        private VigemClient _client;
        private bool _running = true;
        private bool _remapOn = false; // Toggle state

        private const int ToggleButtonIndex = 8;

        public DpadMapper()
        {
            _directInput = new DirectInput();
        }

        public void Run()
        {
            var devices = _directInput.GetDevices(DeviceType.Gamepad, DeviceEnumerationFlags.AttachedOnly)
                .Concat(_directInput.GetDevices(DeviceType.Joystick, DeviceEnumerationFlags.AttachedOnly)).ToList();

            if (devices.Count == 0)
            {
                Console.WriteLine("No gamepad detected.");
                return;
            }

            var deviceInstance = devices[0];
            _joystick = new Joystick(_directInput, deviceInstance.InstanceGuid);
            _joystick.Properties.BufferSize = 128;
            try { _joystick.Acquire(); } catch { Console.WriteLine("Failed to acquire joystick."); return; }

            _client = new VigemClient();
            _xbox = new Xbox360Controller(_client);
            _xbox.Connect();

            Console.WriteLine("Virtual Xbox 360 controller ready.");

            var caps = _joystick.Capabilities;
            int numButtons = caps.ButtonCount;
            int toggleBtn = ToggleButtonIndex;
            if (toggleBtn >= numButtons) toggleBtn = Math.Max(0, numButtons - 1);

            while (_running)
            {
                try
                {
                    _joystick.Poll();
                    var state = _joystick.GetCurrentState();

                    bool togglePressed = false;
                    if (state.Buttons.Length > toggleBtn)
                        togglePressed = state.Buttons[toggleBtn];

                    int pov = -1;
                    if (state.PointOfViewControllers != null && state.PointOfViewControllers.Length > 0)
                        pov = state.PointOfViewControllers[0];

                    bool up = false, down = false, left = false, right = false;

                    if (pov < 0)
                    {
                        var b = state.Buttons;
                        if (b.Length > 15)
                        {
                            up = b[12];
                            down = b[13];
                            left = b[14];
                            right = b[15];
                        }
                        else if (b.Length > 11)
                        {
                            up = b[11];
                            down = b[12];
                            left = b[13];
                            right = b[14];
                        }
                    }
                    else
                    {
                        if (pov == 0) up = true;
                        else if (pov == 9000) right = true;
                        else if (pov == 18000) down = true;
                        else if (pov == 27000) left = true;
                        else
                        {
                            if (pov > 0 && pov < 9000) { up = true; right = true; }
                            else if (pov > 9000 && pov < 18000) { right = true; down = true; }
                            else if (pov > 18000 && pov < 27000) { down = true; left = true; }
                            else if (pov > 27000) { left = true; up = true; }
                        }
                    }

                    short nativeLX = state.X;
                    short nativeLY = state.Y;

                    float lx = nativeLX / 32767f;
                    float ly = nativeLY / 32767f;

                    if (_remapOn)
                    {
                        float dpx = 0, dpy = 0;
                        if (left) dpx = -1;
                        if (right) dpx = 1;
                        if (up) dpy = -1;
                        if (down) dpy = 1;

                        lx = Math.Max(-1, Math.Min(1, lx + dpx));
                        ly = Math.Max(-1, Math.Min(1, ly + dpy));
                    }

                    short outX = (short)(lx * 32767);
                    short outY = (short)(ly * 32767);

                    _xbox.SetAxisValue(Xbox360Axis.LeftThumbX, outX);
                    _xbox.SetAxisValue(Xbox360Axis.LeftThumbY, outY);

                    if (togglePressed)
                    {
                        _remapOn = !_remapOn;
                        Console.WriteLine($"Remap: {(_remapOn ? "ON" : "OFF")}");
                        while (true)
                        {
                            _joystick.Poll();
                            var s2 = _joystick.GetCurrentState();
                            if (!s2.Buttons[toggleBtn]) break;
                            Thread.Sleep(20);
                        }
                    }

                    Thread.Sleep(6);
                }
                catch { Thread.Sleep(200); }
            }
        }
    }
}
