import contextlib
import io
import unittest
from datetime import date

from backend.availability_service import (
    Creneau,
    CreneauStatus,
    DisponibiliteService,
    ResourceType,
    Ressource,
    demo_us01,
)


class CreneauTests(unittest.TestCase):
    def test_validates_hours_and_formats_status(self):
        slot = Creneau(9, 11, CreneauStatus.DISPONIBLE)

        self.assertEqual(repr(slot), "09:00 - 11:00 [✓ disponible]")
        self.assertEqual(
            repr(Creneau(11, 12, CreneauStatus.RESERVE)),
            "11:00 - 12:00 [✗ reservé]",
        )

    def test_rejects_hours_outside_day(self):
        for start, end in ((-1, 1), (0, 24)):
            with self.subTest(start=start, end=end):
                with self.assertRaisesRegex(ValueError, "entre 0 et 23"):
                    Creneau(start, end, CreneauStatus.DISPONIBLE)

    def test_rejects_empty_or_reversed_range(self):
        for start, end in ((9, 9), (10, 9)):
            with self.subTest(start=start, end=end):
                with self.assertRaisesRegex(ValueError, "antérieure"):
                    Creneau(start, end, CreneauStatus.DISPONIBLE)


class ResourceTests(unittest.TestCase):
    def test_stores_slots_and_formats_resource(self):
        resource = Ressource("ROOM-1", "Salle A", ResourceType.SALLE, capacite=8)
        slots = [Creneau(9, 10, CreneauStatus.DISPONIBLE)]
        day = date(2026, 10, 15)

        resource.ajouter_creneaux(day, slots)

        self.assertEqual(resource.horaires[day], slots)
        self.assertEqual(repr(resource), "Ressource(Salle A, type=salle, capacité=8)")


class DisponibiliteServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = DisponibiliteService()
        self.day = date(2026, 10, 15)
        self.room = Ressource("ROOM-1", "Salle A", ResourceType.SALLE)
        self.room.ajouter_creneaux(
            self.day,
            [
                Creneau(9, 11, CreneauStatus.DISPONIBLE),
                Creneau(11, 12, CreneauStatus.RESERVE),
                Creneau(12, 13, CreneauStatus.INDISPONIBLE),
            ],
        )
        self.service.ajouter_ressource(self.room)

    def test_lists_resources_with_optional_type_filter(self):
        computer = Ressource("PC-1", "Ordinateur", ResourceType.ORDINATEUR)
        self.service.ajouter_ressource(computer)

        self.assertEqual(self.service.lister_ressources(), [self.room, computer])
        self.assertEqual(
            self.service.lister_ressources(ResourceType.ORDINATEUR), [computer]
        )
        self.assertEqual(self.service.filtrer_par_type(ResourceType.SALLE), [self.room])

    def test_raises_for_unknown_resource(self):
        with self.assertRaisesRegex(ValueError, "ROOM-404"):
            self.service.consulter_disponibilite("ROOM-404", self.day)

    def test_reports_missing_day_and_applies_default_hours(self):
        result = self.service.consulter_disponibilite("ROOM-1", date(2026, 10, 16))

        self.assertEqual(result["plage_requise"], "00:00 - 23:00")
        self.assertEqual(result["statut"], "Aucune donnée disponible")
        self.assertEqual(result["creneaux"], [])

    def test_reports_missing_day_with_explicit_hours(self):
        result = self.service.consulter_disponibilite(
            "ROOM-1", date(2026, 10, 16), 8, 10
        )

        self.assertEqual(result["plage_requise"], "08:00 - 10:00")

    def test_reports_available_reserved_and_unavailable_overlaps(self):
        result = self.service.consulter_disponibilite("ROOM-1", self.day, 10, 13)

        self.assertEqual(result["nombre_creneaux_disponibles"], 1)
        self.assertEqual(result["nombre_creneaux_indisponibles"], 2)
        self.assertEqual(len(result["creneaux_indisponibles"]), 2)
        self.assertEqual(result["statut_global"], "✗ INDISPONIBLE")

    def test_reports_available_when_all_overlapping_slots_are_free(self):
        result = self.service.consulter_disponibilite("ROOM-1", self.day, 9, 10)

        self.assertEqual(result["statut_global"], "✓ DISPONIBLE")
        self.assertEqual(result["nombre_creneaux_disponibles"], 1)
        self.assertEqual(result["nombre_creneaux_indisponibles"], 0)

    def test_reports_unavailable_when_no_slot_overlaps(self):
        result = self.service.consulter_disponibilite("ROOM-1", self.day, 13, 14)

        self.assertEqual(result["statut_global"], "✗ INDISPONIBLE")
        self.assertEqual(result["creneaux_disponibles"], [])
        self.assertEqual(result["creneaux_indisponibles"], [])


class DemoTests(unittest.TestCase):
    def test_demo_runs(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            demo_us01()

        self.assertIn("US-01", output.getvalue())
        self.assertIn("Test 5", output.getvalue())


if __name__ == "__main__":
    unittest.main()
