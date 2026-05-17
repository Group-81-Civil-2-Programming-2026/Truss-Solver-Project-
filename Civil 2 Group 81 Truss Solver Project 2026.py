# -*- coding: utf-8 -*-
"""
Created on Sat May  9 15:02:23 2026

-
"""



import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np


app = tk.Tk()
app.title('Truss Solver')

menuBar = tk.Menu(app)
app.configure(menu=menuBar)

joints = []
listOfMembers = []
listOfJointNames =[]
# ---------------------------------------------------------------------------

def newModel():
    framePrprts = tk.LabelFrame(app, text='Truss Properties')
    framePrprts.grid(row=0, column=0, padx=5, pady=5)

    label1 = tk.Label(framePrprts, text='Number of Joints')
    label1.grid(row=0, column=0)
    numOfJoint = tk.Entry(framePrprts)
    numOfJoint.grid(row=0, column=1)

    def joint_Proceed():
        global joints
        global listOfJointNames
        value = int(numOfJoint.get())
        joints = [0] * value
        listOfJointNames = []
        for i in range(value):
            listOfJointNames.append('Joint' + str(i + 1))
        comboJoint = ttk.Combobox(framePrprts, values=listOfJointNames)
        comboJoint.grid(row=0, column=3)

        def JointSelected(event):
            inputFrame = tk.LabelFrame(app, text='Supply ' + comboJoint.get() + ' Information')
            inputFrame.grid(row=1, column=0, padx=5, pady=5)

            lbl_ID = tk.Label(inputFrame, text='ID')
            lbl_ID.grid(row=0, column=0)
            ent_ID = tk.Entry(inputFrame)
            ent_ID.grid(row=0, column=1)

            lbl_x = tk.Label(inputFrame, text='X-Coord (m)')
            lbl_x.grid(row=1, column=0)
            ent_x = tk.Entry(inputFrame)
            ent_x.grid(row=1, column=1)

            lbl_y = tk.Label(inputFrame, text='Y-Coord (m)')
            lbl_y.grid(row=2, column=0)
            ent_y = tk.Entry(inputFrame)
            ent_y.grid(row=2, column=1)

            lbl_mag = tk.Label(inputFrame, text='Load Magnitude (kN)')
            lbl_mag.grid(row=3, column=0)
            ent_mag = tk.Entry(inputFrame)
            ent_mag.grid(row=3, column=1)

            lbl_angle = tk.Label(inputFrame, text='Load Angle (deg)')
            lbl_angle.grid(row=4, column=0)
            ent_angle = tk.Entry(inputFrame)
            ent_angle.grid(row=4, column=1)

            lbl_sup = tk.Label(inputFrame, text='Support')
            lbl_sup.grid(row=5, column=0)
            comboSup = ttk.Combobox(inputFrame, values=['None', 'Roller', 'Pin', 'Fixed'], state='readonly')
            comboSup.current(0)
            comboSup.grid(row=5, column=1)

            def saveJoint():
                selected = comboJoint.get()
                joint_ind = int(selected.replace('Joint', '')) - 1
                support = comboSup.get()
                if support == 'None':
                    support = None
                joints[joint_ind] = Joint(ent_ID.get(), ent_x.get(), ent_y.get(),
                                          ent_mag.get(), ent_angle.get(), support)
                messagebox.showinfo('Saved', ent_ID.get() + ' saved successfully')

            saveButton = tk.Button(inputFrame, text='Save', command=saveJoint)
            saveButton.grid(row=6, column=1)

        comboJoint.bind('<<ComboboxSelected>>', JointSelected)

    jointProceed = tk.Button(framePrprts, text='Proceed', command=joint_Proceed)
    jointProceed.grid(row=0, column=2)

    label2 = tk.Label(framePrprts, text='Number of Members')
    label2.grid(row=1, column=0)
    numOfMember = tk.Entry(framePrprts)
    numOfMember.grid(row=1, column=1)

    def memberProceed():
        global listOfMembers
        value = int(numOfMember.get())
        listOfMembers = [0] * value
        memberNames = []
        for i in range(value):
            memberNames.append('Member' + str(i + 1))
        comboMember = ttk.Combobox(framePrprts, values=memberNames)
        comboMember.grid(row=1, column=3)

        def memberSelected(event):
            top = tk.Toplevel()
            frMember = tk.LabelFrame(top, text='Supply Member Information')
            frMember.grid(row=0, column=0, padx=5, pady=5)

            lbl_ID = tk.Label(frMember, text='Member ID')
            lbl_ID.grid(row=0, column=0)
            ent_ID = tk.Entry(frMember)
            ent_ID.grid(row=0, column=1)

            lbl_start = tk.Label(frMember, text='Start Joint')
            lbl_start.grid(row=1, column=0)
            comboStart = ttk.Combobox(frMember, values=listOfJointNames, state='readonly')
            comboStart.grid(row=1, column=1)

            lbl_end = tk.Label(frMember, text='End Joint')
            lbl_end.grid(row=2, column=0)
            comboEnd = ttk.Combobox(frMember, values=listOfJointNames, state='readonly')
            comboEnd.grid(row=2, column=1)

            lbl_area = tk.Label(frMember, text='Area (m2)')
            lbl_area.grid(row=3, column=0)
            ent_area = tk.Entry(frMember)
            ent_area.insert(0, '0.01')
            ent_area.grid(row=3, column=1)

            lbl_E = tk.Label(frMember, text='E - Youngs Modulus (kN/m2)')
            lbl_E.grid(row=4, column=0)
            ent_E = tk.Entry(frMember)
            ent_E.insert(0, '200000000')
            ent_E.grid(row=4, column=1)

            def saveMember():
                selected = comboMember.get()
                mem_ind = int(selected.replace('Member', '')) - 1

                startName = comboStart.get()
                start_ind = int(startName.replace('Joint', '')) - 1

                endName = comboEnd.get()
                end_ind = int(endName.replace('Joint', '')) - 1

                j1 = joints[start_ind]
                j2 = joints[end_ind]
                listOfMembers[mem_ind] = Member(ent_ID.get(), j1, j2, ent_area.get(), ent_E.get())
                messagebox.showinfo('Saved', 'Member ' + ent_ID.get() + ' saved')
                top.destroy()

            saveButton = tk.Button(frMember, text='Save', command=saveMember)
            saveButton.grid(row=5, column=1)

        comboMember.bind('<<ComboboxSelected>>', memberSelected)

    memberProceedBtn = tk.Button(framePrprts, text='Proceed', command=memberProceed)
    memberProceedBtn.grid(row=1, column=2)

    solveButton = tk.Button(framePrprts, text='Solve', command=solveTruss)
    solveButton.grid(row=2, column=1)


# ---------------------------------------------------------------------------
# SECTION 2 - SOLVER (Method of Joints)
# ---------------------------------------------------------------------------

def findReactions():
    # Find pin and roller
    pinJoint = None
    rollerJoint = None
    for j in joints:
        if j.support in ('pin', 'fixed') and pinJoint is None:
            pinJoint = j
        elif j.support == 'roller' and rollerJoint is None:
            rollerJoint = j

    if pinJoint is None or rollerJoint is None:
        messagebox.showerror('Cannot Solve', 'Please define one Pin and one Roller support.')
        return False

    # Take moments about pin to find roller vertical reaction
    momentAboutPin = 0.0
    for j in joints:
        dx = j.x - pinJoint.x
        dy = j.y - pinJoint.y
        momentAboutPin += j.load['Fx'] * (-dy) + j.load['Fy'] * dx

    dx_roller = rollerJoint.x - pinJoint.x
    if abs(dx_roller) < 1e-9:
        messagebox.showerror('Cannot Solve', 'Pin and Roller are vertically aligned, cannot take moments.')
        return False

    Ry_roller = -momentAboutPin / dx_roller
    rollerJoint.reaction_vals['V'] = Ry_roller

    sum_Fx = sum(j.load['Fx'] for j in joints)
    sum_Fy = sum(j.load['Fy'] for j in joints)
    pinJoint.reaction_vals['V'] = -(sum_Fy + Ry_roller)
    pinJoint.reaction_vals['H'] = -sum_Fx
    return True


def methodOfJoints(memberForceOverride=None):
    # memberForceOverride lets us pass in a different load case (used for virtual work)
    # It returns a dictionary of member ID -> force

    # Build net load at each joint
    netLoad = {}
    for j in joints:
        fx = j.load['Fx']
        fy = j.load['Fy']
        if 'H' in j.reaction_vals:
            fx += j.reaction_vals['H']
        if 'V' in j.reaction_vals:
            fy += j.reaction_vals['V']
        netLoad[j.ID] = [fx, fy]

    # If a virtual load case is provided, override netLoad with those values
    if memberForceOverride is not None:
        netLoad = memberForceOverride

    knownForces = {}

    def getUnknownMembers(joint):
        result = []
        for m in listOfMembers:
            if m.ID not in knownForces:
                if m.joint1.ID == joint.ID or m.joint2.ID == joint.ID:
                    result.append(m)
        return result

    def getDirectionFrom(mem, joint):
        if mem.joint1.ID == joint.ID:
            other = mem.joint2
        else:
            other = mem.joint1
        dx = other.x - joint.x
        dy = other.y - joint.y
        L = mem.length
        return dx / L, dy / L

    maxPasses = len(listOfMembers) + 5
    passes = 0

    while len(knownForces) < len(listOfMembers) and passes < maxPasses:
        passes += 1
        solvedThisPass = 0

        for j in joints:
            unknowns = getUnknownMembers(j)

            if len(unknowns) == 0:
                continue

            if len(unknowns) == 1:
                m = unknowns[0]
                cos_a, sin_a = getDirectionFrom(m, j)

                if abs(cos_a) > abs(sin_a):
                    F = -netLoad[j.ID][0] / cos_a
                else:
                    F = -netLoad[j.ID][1] / sin_a

                knownForces[m.ID] = F

                if m.joint1.ID == j.ID:
                    other = m.joint2
                else:
                    other = m.joint1
                cos_o, sin_o = getDirectionFrom(m, other)
                netLoad[other.ID][0] += F * cos_o
                netLoad[other.ID][1] += F * sin_o

                solvedThisPass += 1

            elif len(unknowns) == 2:
                m1, m2 = unknowns
                cos1, sin1 = getDirectionFrom(m1, j)
                cos2, sin2 = getDirectionFrom(m2, j)

                A = np.array([[cos1, cos2],
                              [sin1, sin2]])
                b = np.array([-netLoad[j.ID][0],
                              -netLoad[j.ID][1]])

                if abs(np.linalg.det(A)) < 1e-9:
                    continue

                F1, F2 = np.linalg.solve(A, b)

                knownForces[m1.ID] = F1
                knownForces[m2.ID] = F2

                for m, F in [(m1, F1), (m2, F2)]:
                    if m.joint1.ID == j.ID:
                        other = m.joint2
                    else:
                        other = m.joint1
                    cos_o, sin_o = getDirectionFrom(m, other)
                    netLoad[other.ID][0] += F * cos_o
                    netLoad[other.ID][1] += F * sin_o

                solvedThisPass += 1

        if solvedThisPass == 0:
            return None

    return knownForces


def calcDeflections(realForces):
    # Virtual Work Method (Unit Load Method)
    # For each joint and each direction (x and y), we apply a unit virtual load,
    # find the virtual member forces using method of joints,
    # then compute deflection: delta = sum( F * f * L / (E * A) )

    deflections = {}

    for j in joints:
        deflections[j.ID] = {'dx': 0.0, 'dy': 0.0}

        for direction in ['x', 'y']:
            # Reset all reaction vals for the virtual case
            for jj in joints:
                jj.reaction_vals_virtual = {}

            # Apply virtual unit load at this joint in this direction
            virtualNetLoad = {}
            for jj in joints:
                virtualNetLoad[jj.ID] = [0.0, 0.0]

            if direction == 'x':
                virtualNetLoad[j.ID][0] = 1.0
            else:
                virtualNetLoad[j.ID][1] = 1.0

            # Find the virtual reactions using overall equilibrium
            # (same moment/sum approach as real reactions)
            pinJoint = None
            rollerJoint = None
            for jj in joints:
                if jj.support in ('pin', 'fixed') and pinJoint is None:
                    pinJoint = jj
                elif jj.support == 'roller' and rollerJoint is None:
                    rollerJoint = jj

            # Sum virtual loads
            vFx = 1.0 if direction == 'x' else 0.0
            vFy = 1.0 if direction == 'y' else 0.0

            # Moment about pin from virtual load
            dx_jPin = j.x - pinJoint.x
            dy_jPin = j.y - pinJoint.y
            vMoment = vFx * (-dy_jPin) + vFy * dx_jPin

            dx_roller = rollerJoint.x - pinJoint.x
            if abs(dx_roller) < 1e-9:
                continue

            vRy_roller = -vMoment / dx_roller
            virtualNetLoad[rollerJoint.ID][1] += vRy_roller

            vRy_pin = -(vFy + vRy_roller)
            vRx_pin = -vFx
            virtualNetLoad[pinJoint.ID][0] += vRx_pin
            virtualNetLoad[pinJoint.ID][1] += vRy_pin

            # Solve for virtual member forces using method of joints
            virtualForces = methodOfJoints(memberForceOverride=virtualNetLoad)

            if virtualForces is None:
                continue

            # delta = sum ( F * f * L / (E * A) )
            delta = 0.0
            for m in listOfMembers:
                F = realForces.get(m.ID, 0.0)
                f = virtualForces.get(m.ID, 0.0)
                L = m.length
                E = m.E
                Ar = m.area
                delta += (F * f * L) / (E * Ar)

            if direction == 'x':
                deflections[j.ID]['dx'] = delta
            else:
                deflections[j.ID]['dy'] = delta

    return deflections


def solveTruss():
    if len(joints) == 0 or 0 in joints:
        messagebox.showwarning('Warning', 'Please save all joints before solving.')
        return
    if len(listOfMembers) == 0 or 0 in listOfMembers:
        messagebox.showwarning('Warning', 'Please save all members before solving.')
        return

    n_joints = len(joints)
    n_members = len(listOfMembers)
    n_reactions = sum(len(j.reaction_vars) for j in joints)

    # Determinacy check
    if n_members + n_reactions != 2 * n_joints:
        degree = (n_members + n_reactions) - (2 * n_joints)
        if degree < 0:
            messagebox.showerror('Cannot Solve',
                'This truss is a mechanism (m + r < 2j).\n'
                'Please check your inputs.')
        else:
            messagebox.showerror('Cannot Solve',
                'This truss is statically indeterminate (m + r > 2j).\n'
                'Method of joints only works for determinate trusses.')
        return

    # Step 1: Find reactions
    if not findReactions():
        return

    # Step 2: Solve member forces by method of joints
    knownForces = methodOfJoints()

    if knownForces is None:
        messagebox.showerror('Cannot Solve',
            'Method of joints got stuck.\n'
            'Check that no joint has more than 2 unknowns at each step.')
        return

    # Store forces in member objects
    for m in listOfMembers:
        m.force = knownForces.get(m.ID, 0.0)
        if m.force >= 0:
            m.condition = 'Tension'
        else:
            m.condition = 'Compression'

    # Step 3: Compute deflections using virtual work
    deflections = calcDeflections(knownForces)

    # Store deflections in joint objects
    for j in joints:
        j.dx = deflections[j.ID]['dx']
        j.dy = deflections[j.ID]['dy']

    showResults(deflections)


# ---------------------------------------------------------------------------
# SECTION 3 - RESULTS WINDOW
# ---------------------------------------------------------------------------

def showResults(deflections):
    top = tk.Toplevel()
    top.title('Truss Results')
    frResults = tk.LabelFrame(top, text='Truss Results')
    frResults.grid(row=0, column=0, padx=5, pady=5)

    txtResults = tk.Text(frResults, width=60, height=30, font=('Courier', 10))
    txtResults.grid(row=0, column=0)

    scrollbar = tk.Scrollbar(frResults, command=txtResults.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    txtResults.configure(yscrollcommand=scrollbar.set)

    def write(line):
        txtResults.insert(tk.END, line + '\n')

    write('=' * 50)
    write('  TRUSS RESULTS  -  Method of Joints')
    write('  Statically Determinate')
    write('=' * 50)

    write('')
    write('Member Forces:')
    write('  Member     Force (kN)     Condition')
    write('  ' + '-' * 40)
    for m in listOfMembers:
        write('  ' + m.ID.ljust(10) + str(round(m.force, 4)).ljust(15) + m.condition)

    write('')
    write('Support Reactions:')
    write('  Joint      Direction    Reaction (kN)')
    write('  ' + '-' * 40)
    for j in joints:
        if j.reaction_vals:
            for direction, value in j.reaction_vals.items():
                if direction == 'H':
                    label = 'Horizontal'
                else:
                    label = 'Vertical'
                write('  ' + j.ID.ljust(10) + label.ljust(13) + str(round(value, 4)))

    write('')
    write('Joint Deflections (Virtual Work Method):')
    write('  Joint      dx (m)         dy (m)')
    write('  ' + '-' * 40)
    for j in joints:
        dx = round(deflections[j.ID]['dx'], 6)
        dy = round(deflections[j.ID]['dy'], 6)
        write('  ' + j.ID.ljust(10) + str(dx).ljust(15) + str(dy))

    write('')
    write('Equilibrium Check (should both be 0):')
    total_fx = sum(j.load['Fx'] for j in joints)
    total_fy = sum(j.load['Fy'] for j in joints)
    total_rx = sum(v for j in joints for k, v in j.reaction_vals.items() if k == 'H')
    total_ry = sum(v for j in joints for k, v in j.reaction_vals.items() if k == 'V')
    write('  Sum Fx = ' + str(round(total_fx + total_rx, 6)))
    write('  Sum Fy = ' + str(round(total_fy + total_ry, 6)))

    txtResults.config(state=tk.DISABLED)

    btnFrame = tk.Frame(top)
    btnFrame.grid(row=1, column=0, pady=5)

    closeButton = tk.Button(btnFrame, text='Close', command=top.destroy)
    closeButton.grid(row=0, column=0, padx=5)

    drawButton = tk.Button(btnFrame, text='Show Truss Diagram', command=showDiagram)
    drawButton.grid(row=0, column=1, padx=5)


# ---------------------------------------------------------------------------
# SECTION 4 - GRID CANVAS AND TRUSS DIAGRAM
# ---------------------------------------------------------------------------

def showDiagram():
    top = tk.Toplevel()
    top.title('Truss Diagram')

    frDiagram = tk.LabelFrame(top, text='Truss Diagram')
    frDiagram.grid(row=0, column=0, padx=5, pady=5)

    canvasWidth = 700
    canvasHeight = 500
    padding = 60

    canvas = tk.Canvas(frDiagram, width=canvasWidth, height=canvasHeight, bg='white')
    canvas.grid(row=0, column=0)

    # Work out scale to fit truss on the canvas
    allX = [j.x for j in joints]
    allY = [j.y for j in joints]

    minX = min(allX)
    maxX = max(allX)
    minY = min(allY)
    maxY = max(allY)

    rangeX = maxX - minX if maxX != minX else 1
    rangeY = maxY - minY if maxY != minY else 1

    scaleX = (canvasWidth - 2 * padding) / rangeX
    scaleY = (canvasHeight - 2 * padding) / rangeY
    scale = min(scaleX, scaleY)

    def toCanvas(x, y):
        # Convert real coordinates to canvas pixel coordinates
        # Y is flipped because canvas Y increases downward
        cx = padding + (x - minX) * scale
        cy = canvasHeight - padding - (y - minY) * scale
        return cx, cy

    # Draw grid lines
    gridSpacing = 50
    for gx in range(0, canvasWidth, gridSpacing):
        canvas.create_line(gx, 0, gx, canvasHeight, fill='#e0e0e0')
    for gy in range(0, canvasHeight, gridSpacing):
        canvas.create_line(0, gy, canvasWidth, gy, fill='#e0e0e0')

    # Find max deflection to set a sensible scale factor for deformed shape
    maxDef = 0.0
    for j in joints:
        d = np.sqrt(j.dx**2 + j.dy**2)
        if d > maxDef:
            maxDef = d

    # Scale deformed shape so the biggest deflection is 40 pixels
    if maxDef > 1e-9:
        defScale = 40.0 / maxDef
    else:
        defScale = 1.0

    # Draw original members (grey)
    for m in listOfMembers:
        x1, y1 = toCanvas(m.joint1.x, m.joint1.y)
        x2, y2 = toCanvas(m.joint2.x, m.joint2.y)
        canvas.create_line(x1, y1, x2, y2, fill='grey', width=2, dash=(4, 4))

    # Draw deformed members (blue = tension, red = compression)
    for m in listOfMembers:
        x1 = m.joint1.x + m.joint1.dx * defScale / scale
        y1 = m.joint1.y + m.joint1.dy * defScale / scale
        x2 = m.joint2.x + m.joint2.dx * defScale / scale
        y2 = m.joint2.y + m.joint2.dy * defScale / scale

        cx1, cy1 = toCanvas(x1, y1)
        cx2, cy2 = toCanvas(x2, y2)

        if m.condition == 'Tension':
            colour = 'blue'
        else:
            colour = 'red'

        canvas.create_line(cx1, cy1, cx2, cy2, fill=colour, width=2)
        # Label the force on the member
        midx = (cx1 + cx2) / 2
        midy = (cy1 + cy2) / 2
        canvas.create_text(midx, midy - 8, text=m.ID + ': ' + str(round(m.force, 2)) + ' kN',
                           font=('Arial', 7), fill=colour)

    # Draw original joints (hollow circle)
    jointR = 5
    for j in joints:
        cx, cy = toCanvas(j.x, j.y)
        canvas.create_oval(cx - jointR, cy - jointR, cx + jointR, cy + jointR,
                           outline='grey', fill='white')
        canvas.create_text(cx, cy - 12, text=j.ID, font=('Arial', 8), fill='grey')

    # Draw deformed joints (filled circle)
    for j in joints:
        dx_scaled = j.dx * defScale / scale
        dy_scaled = j.dy * defScale / scale
        cx, cy = toCanvas(j.x + dx_scaled, j.y + dy_scaled)
        canvas.create_oval(cx - jointR, cy - jointR, cx + jointR, cy + jointR,
                           outline='black', fill='black')
        canvas.create_text(cx + 8, cy, text=j.ID, font=('Arial', 8), fill='black')

    # Draw support symbols
    for j in joints:
        cx, cy = toCanvas(j.x, j.y)
        if j.support == 'pin':
            canvas.create_polygon(cx, cy, cx - 10, cy + 15, cx + 10, cy + 15,
                                  outline='black', fill='lightblue')
        elif j.support == 'roller':
            canvas.create_polygon(cx, cy, cx - 10, cy + 15, cx + 10, cy + 15,
                                  outline='black', fill='lightyellow')
            canvas.create_oval(cx - 5, cy + 15, cx + 5, cy + 25,
                               outline='black', fill='lightyellow')

    # Legend
    legendX = canvasWidth - 160
    legendY = 15
    canvas.create_text(legendX, legendY, text='--- Original', fill='grey', anchor='w', font=('Arial', 8))
    canvas.create_text(legendX, legendY + 15, text='--- Tension', fill='blue', anchor='w', font=('Arial', 8))
    canvas.create_text(legendX, legendY + 30, text='--- Compression', fill='red', anchor='w', font=('Arial', 8))
    canvas.create_text(legendX, legendY + 45, text='Deformed shape x' + str(round(defScale, 1)),
                       fill='black', anchor='w', font=('Arial', 8))

    closeButton = tk.Button(top, text='Close', command=top.destroy)
    closeButton.grid(row=1, column=0, pady=5)


# ---------------------------------------------------------------------------
# SECTION 5 - MENU
# ---------------------------------------------------------------------------

fileMenu = tk.Menu(menuBar)
menuBar.add_cascade(label='File', menu=fileMenu)
fileMenu.add_command(label='New Model...', command=newModel)


# ---------------------------------------------------------------------------
# SECTION 6 - CLASSES
# ---------------------------------------------------------------------------

class Joint():
    def __init__(self, ID, x, y, load_mag=None, load_angle=None, support=None):
        self.ID = ID
        self.x = float(x)
        self.y = float(y)
        self.load = {'Fx': 0.0, 'Fy': 0.0}

        if load_mag not in (None, '', '0') and load_angle not in (None, ''):
            angle_rad = np.deg2rad(float(load_angle))
            self.load['Fx'] = float(load_mag) * np.cos(angle_rad)
            self.load['Fy'] = float(load_mag) * np.sin(angle_rad)

        if support is not None:
            self.support = support.lower()
        else:
            self.support = None

        if self.support == 'roller':
            self.reaction_vars = {'V'}
        elif self.support in ('pin', 'fixed'):
            self.reaction_vars = {'H', 'V'}
        else:
            self.reaction_vars = set()

        self.reaction_vals = {}
        self.dx = 0.0
        self.dy = 0.0


class Member():
    def __init__(self, ID, joint1, joint2, area, E):
        self.ID = ID
        self.joint1 = joint1
        self.joint2 = joint2
        self.area = float(area)
        self.E = float(E)
        self.length = self.calcLength()
        self.force = 0.0
        self.condition = 'Unknown'

    def calcLength(self):
        x1 = self.joint1.x
        x2 = self.joint2.x
        y1 = self.joint1.y
        y2 = self.joint2.y
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


app.mainloop()