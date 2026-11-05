const parseSkillsValue = (value) => {
  if (!value) {
    return []
  }

  if (Array.isArray(value)) {
    return value.filter(Boolean)
  }

  if (typeof value === 'string') {
    try {
      const parsed = JSON.parse(value)
      if (Array.isArray(parsed)) {
        return parsed.filter(Boolean)
      }
    } catch {
      return value
        .split(',')
        .map((skill) => skill.trim())
        .filter(Boolean)
    }
  }

  return []
}

export const buildProfileQuery = ({
  name,
  userRole,
  primaryRole,
  bio,
  skills,
  github,
  linkedin,
  portfolio,
  experience,
  resolved,
  answered,
  answersCount,
  profile
} = {}) => {
  const query = {}
  const applyValue = (key, value) => {
    if (value === undefined || value === null || value === '') {
      return
    }
    query[key] = value
  }

  const resolvedPrimaryRole =
    primaryRole ?? profile?.primaryRole ?? userRole ?? profile?.role ?? ''
  const resolvedUserRole = userRole ?? profile?.userRole ?? ''

  applyValue('name', name ?? profile?.fullName)
  applyValue('userRole', resolvedUserRole || undefined)
  applyValue('primaryRole', resolvedPrimaryRole || undefined)
  // legacy field so older fallback logic still works
  applyValue('role', resolvedUserRole || resolvedPrimaryRole || undefined)
  applyValue('bio', bio ?? profile?.bio)

  const mergedSkills = skills ?? profile?.skills
  if (mergedSkills && mergedSkills.length) {
    applyValue('skills', JSON.stringify(mergedSkills))
  }

  applyValue('github', github ?? profile?.githubUrl)
  applyValue('linkedin', linkedin ?? profile?.linkedinUrl)
  applyValue('portfolio', portfolio ?? profile?.portfolioUrl)
  applyValue(
    'experience',
    experience ?? profile?.experienceYears ?? profile?.experience
  )
  applyValue('resolved', resolved ?? profile?.resolvedQuestions)
  const answeredValue =
    answered ??
    answersCount ??
    profile?.answersCount ??
    profile?.answered
  applyValue('answered', answeredValue)

  return query
}

export const parseSkillsParam = (value) => {
  return parseSkillsValue(value)
}

