        # -------------------------------------------------------------------
        # Merge and Split (system_playground implementation)
        # -------------------------------------------------------------------

        # MERGE: merge[(idA, idB), ...]
        if merge:
            for (idA, idB) in merge.get("pairs", []):
                objA = next((o for o in self.state.objects if o.id == idA), None)
                objB = next((o for o in self.state.objects if o.id == idB), None)
                if not objA or not objB:
                    continue

                # Deterministic referent-map union
                merged_referents = {}
                for key in set(objA.referent_map.keys()).union(objB.referent_map.keys()):
                    valsA = objA.referent_map.get(key, [])
                    valsB = objB.referent_map.get(key, [])
                    merged_referents[key] = sorted(set(valsA + valsB))

                # Deterministic anchor merge (mean)
                merged_anchors = [
                    (a + b) / 2 for a, b in zip(objA.anchors, objB.anchors)
                ]

                # Deterministic lineage merge
                merged_lineage = {
                    "parent": None,
                    "history": objA.lineage.get("history", []) +
                               objB.lineage.get("history", []) +
                               [f"merge({idA},{idB})"]
                }

                # Deterministic ordering merge (max of each metric)
                merged_ordering = {
                    "recency": max(objA.ordering_metrics["recency"],
                                   objB.ordering_metrics["recency"]),
                    "frequency": max(objA.ordering_metrics["frequency"],
                                     objB.ordering_metrics["frequency"]),
                    "density": max(objA.ordering_metrics["density"],
                                   objB.ordering_metrics["density"]),
                }

                # Create merged object
                merged_obj = IdentityObject(
                    id=f"{idA}_{idB}_merged",
                    referent_map=merged_referents,
                    anchors=merged_anchors,
                    lineage=merged_lineage,
                    ambiguity={"certainty": "medium", "ambiguity": "medium"},
                    stability_metrics={"drift": 0.0, "oscillation": 0.0,
                                       "collapse": False, "frozen": False},
                    ordering_metrics=merged_ordering,
                )

                # Replace A and B with merged object
                self.state.objects.remove(objA)
                self.state.objects.remove(objB)
                self.state.objects.append(merged_obj)

        # SPLIT: split[idX, ...]
        if split:
            for idX in split.get("objects", []):
                objX = next((o for o in self.state.objects if o.id == idX), None)
                if not objX:
                    continue

                # Deterministic referent partition:
                keys = sorted(objX.referent_map.keys())
                half = len(keys) // 2
                keys1 = keys[:half]
                keys2 = keys[half:]

                referents1 = {k: objX.referent_map[k] for k in keys1}
                referents2 = {k: objX.referent_map[k] for k in keys2}

                # Deterministic anchor fork (slight perturbation)
                anchors1 = [a * 0.95 for a in objX.anchors]
                anchors2 = [a * 1.05 for a in objX.anchors]

                # Deterministic lineage fork
                lineage1 = {
                    "parent": objX.id,
                    "history": objX.lineage.get("history", []) + [f"split({idX})_1"]
                }
                lineage2 = {
                    "parent": objX.id,
                    "history": objX.lineage.get("history", []) + [f"split({idX})_2"]
                }

                # Ordering propagation
                ordering1 = {
                    "recency": objX.ordering_metrics["recency"],
                    "frequency": objX.ordering_metrics["frequency"],
                    "density": objX.ordering_metrics["density"],
                }
                ordering2 = ordering1.copy()

                # Create split objects
                objX1 = IdentityObject(
                    id=f"{idX}_1",
                    referent_map=referents1,
                    anchors=anchors1,
                    lineage=lineage1,
                    ambiguity=objX.ambiguity.copy(),
                    stability_metrics={"drift": 0.0, "oscillation": 0.0,
                                       "collapse": False, "frozen": False},
                    ordering_metrics=ordering1,
                )

                objX2 = IdentityObject(
                    id=f"{idX}_2",
                    referent_map=referents2,
                    anchors=anchors2,
                    lineage=lineage2,
                    ambiguity=objX.ambiguity.copy(),
                    stability_metrics={"drift": 0.0, "oscillation": 0.0,
                                       "collapse": False, "frozen": False},
                    ordering_metrics=ordering2,
                )

                # Replace original with split objects
                self.state.objects.remove(objX)
                self.state.objects.append(objX1)
                self.state.objects.append(objX2)
