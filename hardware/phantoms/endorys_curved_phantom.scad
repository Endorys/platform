// ENDORYS Platform — Protocol E001 Parametric Curved-Surface Phantom Mold & Probe Cradle
// License: CC-BY-4.0 (Documentation & Reference Test Fixtures)
// Note: Commercial hardware & closed-loop CQI gating patent rights reserved (IN 202641134091).

$fn = 120;
radius_mm         = 60.0;  // 35, 60, or 90 mm
phantom_width_mm  = 90.0;
phantom_depth_mm  = 65.0;
wall_thickness_mm = 4.0;
hydrogel_slot_mm  = 3.0;
wire_target_d_mm  = 0.5;

module curved_phantom_mold(r_mm = radius_mm) {
    outer_w = phantom_width_mm + 2 * wall_thickness_mm;
    outer_d = phantom_depth_mm + wall_thickness_mm;
    sagitta = r_mm - sqrt(max(1, r_mm * r_mm - pow(phantom_width_mm / 2, 2)));

    difference() {
        translate([-outer_w / 2, -25, 0])
            cube([outer_w, 50, outer_d + sagitta]);
        translate([-phantom_width_mm / 2, -21, wall_thickness_mm])
            cube([phantom_width_mm, 42, phantom_depth_mm + sagitta + 2]);
        translate([0, 0, wall_thickness_mm + phantom_depth_mm + r_mm])
            rotate([90, 0, 0])
                cylinder(h = 60, r = r_mm, center = true);
        for (z_off =) {
            translate([0, 0, wall_thickness_mm + z_off])
                rotate([90, 0, 0])
                    cylinder(h = 60, d = wire_target_d_mm + 0.3, center = true);
        }
    }
}

curved_phantom_mold(radius_mm);
