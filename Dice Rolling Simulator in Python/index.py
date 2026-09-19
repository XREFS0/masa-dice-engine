"""
MASA Quantum Dice Simulator & Probability Engine
Developer: MASA
"""

import random
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MasaDiceEngine(ctk.CTk):
    DOT_COORDS = {
        1: [(75, 75)],
        2: [(45, 45), (105, 105)],
        3: [(40, 40), (75, 75), (110, 110)],
        4: [(45, 45), (105, 45), (45, 105), (105, 105)],
        5: [(45, 45), (105, 45), (75, 75), (45, 105), (105, 105)],
        6: [(45, 38), (105, 38), (45, 75), (105, 75), (45, 112), (105, 112)],
    }

    def __init__(self):
        super().__init__()

        self.title("MASA Dice Engine")
        self.geometry("440x600")
        self.resizable(False, False)
        self.configure(fg_color="#0B0F19")

        self.dice_count = 1
        self.history = []
        self._animating = False

        self._build_ui()
        self._draw_dice(1, [1])

    def _build_ui(self):
        header_card = ctk.CTkFrame(self, fg_color="#121829", corner_radius=14)
        header_card.pack(fill="x", padx=20, pady=(20, 15))

        title = ctk.CTkLabel(
            header_card,
            text="MASA PROBABILITY SIMULATOR",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#818CF8",
        )
        title.pack(pady=(12, 2))

        subtitle = ctk.CTkLabel(
            header_card,
            text="High-Fidelity Quantum Dice Roller",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8",
        )
        subtitle.pack(pady=(0, 12))

        controls_row = ctk.CTkFrame(self, fg_color="#121829", corner_radius=12)
        controls_row.pack(fill="x", padx=20, pady=(0, 10))

        lbl_mode = ctk.CTkLabel(controls_row, text="DICE COUNT", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94A3B8")
        lbl_mode.pack(side="left", padx=16, pady=10)

        self.seg_btn = ctk.CTkSegmentedButton(
            controls_row,
            values=["1 Die", "2 Dice"],
            command=self._on_count_change,
            selected_color="#6366F1",
            selected_hover_color="#4F46E5",
        )
        self.seg_btn.set("1 Die")
        self.seg_btn.pack(side="right", padx=16, pady=8)

        self.arena_card = ctk.CTkFrame(self, fg_color="#121829", corner_radius=16)
        self.arena_card.pack(fill="x", padx=20, pady=5)

        self.canvas = ctk.CTkCanvas(self.arena_card, width=360, height=170, bg="#121829", highlightthickness=0)
        self.canvas.pack(pady=15)

        self.score_lbl = ctk.CTkLabel(
            self.arena_card,
            text="Total: 1",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F8FAFC",
        )
        self.score_lbl.pack(pady=(0, 15))

        self.roll_btn = ctk.CTkButton(
            self,
            text="ROLL THE DICE",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#6366F1",
            hover_color="#4F46E5",
            height=46,
            corner_radius=12,
            command=self._start_roll,
        )
        self.roll_btn.pack(fill="x", padx=20, pady=12)

        history_card = ctk.CTkFrame(self, fg_color="#121829", corner_radius=14)
        history_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        lbl_hist = ctk.CTkLabel(history_card, text="ROLL HISTORY", font=ctk.CTkFont(size=11, weight="bold"), text_color="#64748B")
        lbl_hist.pack(anchor="w", padx=16, pady=(10, 4))

        self.history_box = ctk.CTkTextbox(
            history_card,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#0B0F19",
            corner_radius=10,
        )
        self.history_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _on_count_change(self, val):
        self.dice_count = 1 if val == "1 Die" else 2
        self._draw_dice(self.dice_count, [1] if self.dice_count == 1 else [1, 1])
        self.score_lbl.configure(text=f"Total: {self.dice_count}")

    def _render_die(self, cx, cy, val):
        size = 120
        x1, y1 = cx - size // 2, cy - size // 2
        x2, y2 = cx + size // 2, cy + size // 2

        self.canvas.create_rectangle(x1 + 4, y1 + 4, x2 + 4, y2 + 4, fill="#070A10", width=0)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#1E2638", outline="#4F46E5", width=2)

        dots = self.DOT_COORDS.get(val, [])
        for dx, dy in dots:
            actual_x = x1 + (dx / 150.0) * size
            actual_y = y1 + (dy / 150.0) * size
            r = 6
            self.canvas.create_oval(
                actual_x - r, actual_y - r, actual_x + r, actual_y + r,
                fill="#38BDF8", outline="#E0F2FE", width=1,
            )

    def _draw_dice(self, count, values):
        self.canvas.delete("all")
        if count == 1:
            self._render_die(180, 85, values[0])
        else:
            self._render_die(105, 85, values[0])
            self._render_die(255, 85, values[1])

    def _start_roll(self):
        if self._animating:
            return
        self._animating = True
        self.roll_btn.configure(state="disabled")
        self._animate_roll(0, 12)

    def _animate_roll(self, step, total_steps):
        vals = [random.randint(1, 6) for _ in range(self.dice_count)]
        self._draw_dice(self.dice_count, vals)

        if step < total_steps:
            delay = 40 + step * 10
            self.after(delay, lambda: self._animate_roll(step + 1, total_steps))
        else:
            final_vals = [random.randint(1, 6) for _ in range(self.dice_count)]
            self._draw_dice(self.dice_count, final_vals)
            total = sum(final_vals)
            self.score_lbl.configure(text=f"Total: {total} ({', '.join(map(str, final_vals))})")

            log_entry = f"Roll #{len(self.history) + 1:02d} => {final_vals} (Sum: {total})\n"
            self.history.append(log_entry)
            self.history_box.insert("0.0", log_entry)

            self._animating = False
            self.roll_btn.configure(state="normal")


if __name__ == "__main__":
    app = MasaDiceEngine()
    app.mainloop()
