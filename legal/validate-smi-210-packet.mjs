#!/usr/bin/env node
/**
 * Operator checks for the SMI-210 SAFESHOT ITU packet.
 * Fails if the packet drifts into Class 32, free-form IDs, or drops neighbor TSDR links.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)));
const fields = JSON.parse(readFileSync(join(root, "smi-210-trademark-center-fields.json"), "utf8"));
const packet = readFileSync(join(root, "smi-210-safeshot-itu-counsel-packet.md"), "utf8");
const email = readFileSync(join(root, "smi-210-counsel-cover-email.md"), "utf8");

const errors = [];
const check = (ok, msg) => {
  if (!ok) errors.push(msg);
};

check(fields.application.mark === "SAFESHOT", "mark must be SAFESHOT");
check(fields.application.mark_type === "standard_character", "must be standard character");
check(fields.application.filing_basis === "1b", "must be §1(b)");
check(fields.application.combined_with_sideshot === false, "must not combine with SIDESHOT app");
check(fields.application.disclaimer === null, "no disclaimer at filing");
check(fields.application.significance_statement === null, "no significance statement");

const classNums = fields.classes.map((c) => c.international_class).sort();
check(classNums.join(",") === "008,021", `classes must be 008+021, got ${classNums.join(",")}`);
check(fields.forbidden_classes.includes("032"), "Class 32 must be forbidden");
check(fields.fees_usd.uspto_total === 700, "USPTO total must be $700");

for (const cls of fields.classes) {
  check(cls.id_manual_only === true, `${cls.international_class} must be ID Manual only`);
  check(cls.character_count === cls.identification.length, `${cls.international_class} character_count mismatch`);
  check(cls.character_count < 1000, `${cls.international_class} ID over 1000 chars`);
  const lower = cls.identification.toLowerCase();
  for (const bad of ["shotgun", "beer", "ale", "malt", "target hanger"]) {
    check(!lower.includes(bad), `${cls.international_class} ID contains forbidden "${bad}"`);
  }
}

check(
  fields.classes[0].identification ===
    "Hand tools, namely, punches; Hand-operated cutting tools; Can openers, non-electric",
  "Class 8 ID string drifted"
);
check(
  fields.classes[1].identification === "Bottle openers, electric and non-electric",
  "Class 21 ID string drifted"
);

const neighborSerials = fields.neighbors.map((n) => n.serial).sort();
check(neighborSerials.includes("97037634"), "missing SAFESHOT neighbor SN 97037634");
check(neighborSerials.includes("98831421"), "missing SURE SHOT neighbor SN 98831421");
check(fields.neighbors[0].registration === "8061021", "missing RN 8061021");

for (const n of fields.neighbors) {
  check(typeof n.tsdr === "string" && n.tsdr.includes(n.serial), `TSDR missing serial ${n.serial}`);
  check(n.tsdr.startsWith("https://tsdr.uspto.gov/"), `TSDR not USPTO for ${n.serial}`);
}

check(fields.serial_number === null, "packet must not invent a serial number");
check(fields.tsdr_after_filing === null, "packet must not invent a post-filing TSDR");

for (const text of [packet, email]) {
  check(/Class(?:es)?\s+\*\*008 \+ 021|\*\*8 and 21|\*\*008 \+ 021|Classes 8 \+ 21|Classes:\s+8 and 21|008 \+ 021 only/i.test(text) || text.includes("8 + 21") || text.includes("8 and 21"), "doc must state Classes 8 + 21");
  check(/Do \*\*not\*\* claim Class 32|Never Class 32|Do \*\*not\*\* claim Class 32/i.test(text) || text.includes("not** claim Class 32") || text.includes("Never Class 32") || text.includes("off Class 32") || text.includes("Class 32"), "doc must address Class 32 ban");
  check(text.includes("97037634"), "doc missing SN 97037634");
  check(text.includes("8061021"), "doc missing RN 8061021");
  check(text.includes("98831421"), "doc missing SN 98831421");
  check(text.includes("tsdr.uspto.gov"), "doc missing TSDR host");
  check(!/\bserial number\b.*\b9\d{7}\b/i.test(text) || text.includes("serial number + TSDR"), "ok");
}

check(packet.includes("Do not enter Class 6") || packet.includes("Never Class 6"), "packet must bar Class 6");
check(packet.includes("2(e)(1)"), "packet must brief 2(e)(1)");
check(packet.includes("Supplemental Register"), "packet must include Supplemental fallback");
check(email.includes("$700"), "cover email must state $700 fee");

if (errors.length) {
  console.error(`SMI-210 packet validation FAILED (${errors.length})`);
  for (const e of errors) console.error(` - ${e}`);
  process.exit(1);
}

console.log("SMI-210 packet validation passed");
console.log(` mark=${fields.application.mark} basis=${fields.application.filing_basis} classes=${classNums.join("+")}`);
console.log(` uspto_fee=$${fields.fees_usd.uspto_total} serial=${fields.serial_number}`);
console.log(` neighbors=${neighborSerials.join(", ")}`);
